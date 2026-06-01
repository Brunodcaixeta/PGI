import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.utils.timezone import make_aware
from django.db import transaction
from pgi.models import User, Eixo, Area, AcaoInstitucional, Etapa, AtualizacaoAcao, AtualizacaoEtapa

class Command(BaseCommand):
    help = 'Importa os dados refinados dos arquivos CSV para o banco de dados do Django.'

    def parse_number(self, val):
        if not val:
            return None
        # Replace comma with dot for decimals
        val = val.replace(',', '.')
        try:
            return float(val)
        except ValueError:
            return None

    def parse_date(self, date_str):
        if not date_str:
            return None
        try:
            # Example: "May 27, 2025 5:52 pm"
            date_obj = datetime.strptime(date_str.strip(), "%b %d, %Y %I:%M %p")
            return make_aware(date_obj)
        except ValueError:
            return None

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Limpando banco de dados (flush)..."))
        call_command('flush', interactive=False)
        
        csvs_dir = os.path.join(settings.BASE_DIR, 'csvs', 'novos')

        # Dicionários em memória para acelerar pesquisas
        user_email_map = {}

        # 1. Usuários
        self.stdout.write("Importando Usuários...")
        with open(os.path.join(csvs_dir, 'tabela_usuarios.csv'), newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                is_gestor = row.get('gestor_chefe', '').strip().lower() in ['sim', 'true', '1']
                is_admin = row.get('suporte_admin', '').strip().lower() in ['sim', 'true', '1']
                
                if is_admin:
                    perfil = 'adm'
                elif is_gestor:
                    perfil = 'gestor'
                else:
                    perfil = 'leitor'

                email = row['email'].strip()
                username = email.split('@')[0] if email else f"user_{row['id_user']}"
                
                user = User(
                    id=int(row['id_user']),
                    username=username,
                    email=email,
                    first_name=row.get('nome', '').strip(),
                    last_name=row.get('sobrenome', '').strip(),
                    perfil=perfil,
                    is_staff=is_admin,
                    is_superuser=is_admin,
                )
                user.set_password('mpgo123')
                user.save()
                user_email_map[email] = user.id


        # 3. Eixos
        self.stdout.write("Importando Eixos...")
        with open(os.path.join(csvs_dir, 'tabela_eixos.csv'), newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                Eixo.objects.create(
                    id=int(row['id_eixo']),
                    eixo=row['eixo'].strip()
                )

        # 4. Áreas
        self.stdout.write("Importando Áreas...")
        with open(os.path.join(csvs_dir, 'tabela_areas.csv'), newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                atuacao_fim = row.get('atuacao', '').strip().lower() in ['área fim', 'area fim', 'true', 'sim']
                Area.objects.create(
                    id=int(row['id_area']),
                    sigla=row.get('sigla', '').strip(),
                    nome_area=row.get('nome_area', '').strip(),
                    atuacao=atuacao_fim
                )

        # 5. Ações Institucionais
        self.stdout.write("Importando Ações Institucionais...")
        acao_codigo_map = {}
        with open(os.path.join(csvs_dir, 'tabela_acoes.csv'), newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                try:
                    area_id = int(row['id_area'])
                    responsavel_id = int(row['id_user']) if row.get('id_user') else None
                    
                    acao = AcaoInstitucional.objects.create(
                        acao=row['acao'].strip(),
                        codigo=row.get('codigo_acao', '').strip(),
                        ordem=int(row['ordem']) if row.get('ordem') else None,
                        eixo_id=int(row['id_eixo']),
                        area_id=area_id,
                        responsavel_id=responsavel_id,
                    )
                    acao_codigo_map[acao.codigo] = acao.id
                    
                    # Vínculo automático: se o usuário for responsável por esta ação, atualiza sua área e perfil
                    if responsavel_id:
                        user = User.objects.get(id=responsavel_id)
                        if not user.area_id:
                            user.area_id = area_id
                            if user.perfil == 'leitor':
                                user.perfil = 'editor'
                            user.save()
                            
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(f"Erro ao importar ação {row.get('codigo_acao')}: {e}"))

        # 6. Etapas
        self.stdout.write("Importando Etapas...")
        etapa_codigo_map = {}
        with open(os.path.join(csvs_dir, 'tabela_etapas.csv'), newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                codigo_acao = row.get('codigo_acao', '').strip()
                acao_id = acao_codigo_map.get(codigo_acao)
                if not acao_id:
                    continue
                
                etapa_ref = row.get('id_etapa', '').strip()
                concluido = row.get('concluido', '').strip().lower() in ['sim', 'true', '1']
                ordem_raw = row.get('ordem', '').strip()
                
                # Regra Sênior: Identificar se o registro é um rascunho/deletado herdado do sistema legado
                # (Registros sem ordem definida ou cuja referência termina em hífen, ex: 'AI85-')
                bl_deletado = False
                if not ordem_raw or etapa_ref.endswith('-'):
                    bl_deletado = True
                
                responsavel_id = int(row['id_user']) if row.get('id_user') else None
                etapa = Etapa.objects.create(
                    acao_id=acao_id,
                    etapa=row['etapa'].strip(),
                    etapa_referencia=etapa_ref,
                    ordem=int(ordem_raw) if ordem_raw else None,
                    concluido=concluido,
                    responsavel_id=responsavel_id,
                    bl_deletado=bl_deletado,
                )
                etapa_codigo_map[etapa_ref] = etapa.id
                
                # Vínculo automático: se o usuário for responsável por esta etapa, atualiza sua área e perfil baseado na ação
                if responsavel_id:
                    user = User.objects.get(id=responsavel_id)
                    if not user.area_id:
                        # Busca o ID da área a partir do mapeamento de ações
                        acao_obj = AcaoInstitucional.objects.get(id=acao_id)
                        user.area_id = acao_obj.area_id
                        if user.perfil == 'leitor':
                            user.perfil = 'editor'
                        user.save()

        # 7. Atualizações das Ações
        self.stdout.write("Importando Atualizações de Ações...")
        if os.path.exists(os.path.join(csvs_dir, 'tabela_atualizacao_acoes.csv')):
            with open(os.path.join(csvs_dir, 'tabela_atualizacao_acoes.csv'), newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    codigo_acao = row.get('codigo_acao', '').strip()
                    acao_id = acao_codigo_map.get(codigo_acao)
                    if not acao_id:
                        continue
                    
                    email_resp = row.get('resp_alteracao', '').strip()
                    resp_id = user_email_map.get(email_resp)

                    upd = AtualizacaoAcao.objects.create(
                        acao_id=acao_id,
                        valor_anterior=self.parse_number(row.get('valor_anterior')),
                        valor_evolucao=self.parse_number(row.get('valor_evolucao')),
                        responsavel_registro_id=resp_id,
                    )
                    date_obj = self.parse_date(row.get('data_modificacao'))
                    if date_obj:
                        AtualizacaoAcao.objects.filter(id=upd.id).update(data_atualizacao=date_obj)

        # 8. Atualizações das Etapas
        self.stdout.write("Importando Atualizações de Etapas...")
        if os.path.exists(os.path.join(csvs_dir, 'tabela_atualizacao_etapas.csv')):
            with open(os.path.join(csvs_dir, 'tabela_atualizacao_etapas.csv'), newline='', encoding='utf-8') as f:
                for row in csv.DictReader(f):
                    etapa_id = etapa_codigo_map.get(row.get('id_etapa', '').strip())
                    if not etapa_id:
                        continue
                    
                    progresso = row.get('progresso_entrega', '').strip()
                    obs = row.get('observacoes', '').strip()
                    if obs:
                        progresso = f"{progresso}\n\nObservações: {obs}"

                    upd = AtualizacaoEtapa.objects.create(
                        etapa_id=etapa_id,
                        progresso_entrega=progresso,
                        responsavel_registro_id=int(row['id_user']) if row.get('id_user') else None,
                    )
                    
                    date_obj = self.parse_date(row.get('data_atualizacao'))
                    if date_obj:
                        AtualizacaoEtapa.objects.filter(id=upd.id).update(data_atualizacao=date_obj)

        # 9. Resetar Sequences (Auto-incremento) do PostgreSQL
        self.stdout.write("Sincronizando IDs automáticos (Sequences)...")
        from django.db import connection
        from django.apps import apps
        from django.core.management.color import no_style
        
        sequence_sql = connection.ops.sequence_reset_sql(no_style(), apps.get_models())
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)

        # 10. Recriar Superuser
        self.stdout.write(self.style.WARNING("Criando Superuser admin/admin123..."))
        User.objects.create_superuser('admin', 'admin@mpgo.mp.br', 'admin123')

        self.stdout.write(self.style.SUCCESS('\nImportação concluída com sucesso! Todos os dados estão no PostgreSQL.'))
