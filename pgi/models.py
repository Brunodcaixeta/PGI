from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PERFIL_CHOICES = [
        ('adm', 'Administrador'),
        ('gestor', 'Gestor'),
        ('editor', 'Editor'),
        ('leitor', 'Leitor'),
    ]

    matricula = models.CharField('Matrícula', max_length=50, blank=True, null=True)
    perfil = models.CharField('Perfil', max_length=10, choices=PERFIL_CHOICES, default='leitor')
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Área', related_name='usuarios')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'users'

    def get_full_name(self):
        from pgi.utils import remover_duplicados_nome
        full_name = f"{self.first_name} {self.last_name}".strip()
        return remover_duplicados_nome(full_name)

    def __str__(self):
        full_name = self.get_full_name()
        return full_name if full_name else self.username

    def pode_escrever_na_area(self, area_id):
        if not self.is_authenticated:
            return False
        if self.is_superuser or self.perfil == 'adm' or self.perfil == 'gestor':
            return True
        if self.perfil == 'editor' and self.area_id and self.area_id == area_id:
            return True
        return False

    def pode_escrever_na_acao(self, acao):
        return self.pode_escrever_na_area(acao.area_id)



class Eixo(models.Model):
    eixo = models.CharField('Eixo', max_length=255)
    evolucao = models.DecimalField('Evolução', max_digits=5, decimal_places=2, null=True, blank=True)
    imagem = models.TextField('Imagem', blank=True, null=True)
    imagem_branco = models.TextField('Imagem (Branco)', blank=True, null=True)
    imagem_escuro = models.TextField('Imagem (Escuro)', blank=True, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Eixo'
        verbose_name_plural = 'Eixos'
        db_table = 'pgi_eixos'

    def __str__(self):
        return self.eixo


class Area(models.Model):
    # Choices para o campo atuação
    TIPO_ATUACAO = [
        (True, 'Área Fim'),
        (False, 'Área Meio'),
    ]

    sigla = models.CharField('Sigla', max_length=50, blank=True, null=True)
    nome_area = models.CharField('Nome da Área', max_length=255)
    atuacao = models.BooleanField('Atuação (Fim / Meio)', choices=TIPO_ATUACAO, default=False)
    
    # Campo fechado para edição manual. Será atualizado por cálculos do sistema ou pode ser substituído por uma @property no futuro.
    pgi_evolucao = models.DecimalField('Evolução PGI', max_digits=5, decimal_places=2, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        db_table = 'area'

    def __str__(self):
        return self.nome_area

    @property
    def calcular_evolucao_dinamica(self):
        # Aqui, no futuro, faremos o cálculo: 
        # soma da evolução das Ações Institucionais vinculadas / quantidade de ações
        # return self.acoes.aggregate(models.Avg('algum_campo'))['algum_campo__avg']
        pass


class AcaoInstitucional(models.Model):
    eixo = models.ForeignKey(Eixo, on_delete=models.PROTECT, related_name='acoes')
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='acoes')
    acao = models.TextField('Ação')
    codigo = models.CharField('Código', max_length=50, blank=True, null=True)
    ordem = models.IntegerField('Ordem', null=True, blank=True)
    # Suplan e Responsável usam o modelo de User
    responsavel_suplan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='acoes_suplan')
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='acoes_responsavel')
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Ação Institucional'
        verbose_name_plural = 'Ações Institucionais'
        db_table = 'pgi_acao_institucional'

    def __str__(self):
        return f"{self.codigo} - {self.acao}"[:100]


class Etapa(models.Model):
    acao = models.ForeignKey(AcaoInstitucional, on_delete=models.CASCADE, related_name='etapas')
    etapa = models.TextField('Etapa')
    etapa_referencia = models.CharField('Etapa Referência', max_length=255, blank=True, null=True)
    ordem = models.IntegerField('Ordem', null=True, blank=True)
    concluido = models.BooleanField('Concluído', default=False)
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='etapas_responsavel')
    bl_deletado = models.BooleanField('Deletado', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        db_table = 'pgi_etapas'

    def __str__(self):
        return self.etapa[:100]


class AtualizacaoAcao(models.Model):
    acao = models.ForeignKey(AcaoInstitucional, on_delete=models.CASCADE, related_name='atualizacoes')
    data_atualizacao = models.DateTimeField('Data da Atualização', auto_now_add=True)
    valor_anterior = models.DecimalField('Valor Anterior', max_digits=5, decimal_places=2, null=True, blank=True)
    valor_evolucao = models.DecimalField('Valor Evolução', max_digits=5, decimal_places=2, null=True, blank=True)
    ultima_atualiz_percentual = models.BooleanField('Última Atualização Percentual', default=False)
    atualizacao_percentual = models.BooleanField('Atualização Percentual', default=False)
    tipo_entrega_marco = models.BooleanField('Tipo Entrega Marco', default=False)
    progresso_entrega = models.TextField('Progresso da Entrega', blank=True, null=True)
    responsavel_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='atualizacoes_acoes_registradas')

    class Meta:
        verbose_name = 'Atualização da Ação'
        verbose_name_plural = 'Atualizações das Ações'
        db_table = 'pgi_atualizacao_acao'


class AtualizacaoEtapa(models.Model):
    etapa = models.ForeignKey(Etapa, on_delete=models.CASCADE, related_name='atualizacoes')
    data_atualizacao = models.DateTimeField('Data da Atualização', auto_now_add=True)
    progresso_entrega = models.TextField('Progresso da Entrega')
    responsavel_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='atualizacoes_etapas_registradas')
    sigla = models.CharField('Sigla', max_length=50, blank=True, null=True)
    bl_deletado = models.BooleanField('Deletado', default=False)

    class Meta:
        verbose_name = 'Atualização da Etapa'
        verbose_name_plural = 'Atualizações das Etapas'
        db_table = 'atualizacao_etapa'
