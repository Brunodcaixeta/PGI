from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, UserAssessor, Eixo, Area, AcaoInstitucional,
    Etapa, AtualizacaoAcao, AtualizacaoEtapa
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Adicionando os campos customizados na tela de edição do Admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações do Módulo PGI', {'fields': ('matricula', 'admin', 'gestor_chefe', 'suporte_admin')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'matricula', 'gestor_chefe', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'matricula')


@admin.register(UserAssessor)
class UserAssessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'titular', 'assessor')
    search_fields = ('titular__username', 'assessor__username', 'titular__first_name', 'assessor__first_name')


@admin.register(Eixo)
class EixoAdmin(admin.ModelAdmin):
    list_display = ('id', 'eixo', 'evolucao', 'created_at')
    search_fields = ('eixo',)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sigla', 'nome_area', 'atuacao', 'pgi_evolucao')
    list_filter = ('atuacao',)
    search_fields = ('sigla', 'nome_area')


@admin.register(AcaoInstitucional)
class AcaoInstitucionalAdmin(admin.ModelAdmin):
    list_display = ('id', 'codigo', 'acao', 'eixo', 'area', 'responsavel')
    list_filter = ('eixo', 'area')
    search_fields = ('codigo', 'acao')


@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ('id', 'acao', 'etapa', 'concluido', 'responsavel')
    list_filter = ('concluido',)
    search_fields = ('etapa',)


@admin.register(AtualizacaoAcao)
class AtualizacaoAcaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'acao', 'data_atualizacao', 'valor_evolucao', 'responsavel_registro')
    list_filter = ('data_atualizacao',)


@admin.register(AtualizacaoEtapa)
class AtualizacaoEtapaAdmin(admin.ModelAdmin):
    list_display = ('id', 'etapa', 'data_atualizacao', 'progresso_entrega', 'responsavel_registro')
    list_filter = ('data_atualizacao',)
