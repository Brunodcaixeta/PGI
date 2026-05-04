from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # O AbstractUser já traz os campos padrão: username, first_name (Nome), last_name (sobrenome), email, password, date_joined (created_at).
    # Abaixo adicionamos apenas os campos específicos do seu diagrama.
    matricula = models.CharField('Matrícula', max_length=50, blank=True, null=True)
    admin = models.BooleanField('Admin', default=False)
    gestor_chefe = models.BooleanField('Gestor Chefe', default=False)
    suporte_admin = models.BooleanField('Suporte Admin', default=False)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'users'

    def __str__(self):
        # Tenta usar o nome completo primeiro, senão cai para o username
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


class UserAssessor(models.Model):
    titular = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessores_do_titular')
    assessor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='titulares_assessorados')

    class Meta:
        verbose_name = 'Assessor de Usuário'
        verbose_name_plural = 'Assessores de Usuários'
        db_table = 'user_assessores'

    def __str__(self):
        return f"{self.assessor} auxilia {self.titular}"


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
