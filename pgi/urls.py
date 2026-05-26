from django.urls import path
from . import views

app_name = 'pgi'

urlpatterns = [
    path('', views.home, name='home'),
    path('eixo/<int:eixo_id>/', views.eixo_detail, name='eixo_detail'),
    path('acao/<int:acao_id>/atualizar/', views.atualizar_evolucao, name='atualizar_evolucao'),
    path('acao/<int:acao_id>/etapa/criar/', views.criar_etapa, name='criar_etapa'),
    path('etapa/<int:etapa_id>/excluir/', views.excluir_etapa, name='excluir_etapa'),
    path('etapa/<int:etapa_id>/toggle-concluido/', views.toggle_concluido_etapa, name='toggle_concluido_etapa'),
]
