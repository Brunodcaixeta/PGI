from django.urls import path
from . import views

app_name = 'pgi'

urlpatterns = [
    path('', views.home, name='home'),
    path('eixo/<int:eixo_id>/', views.eixo_detail, name='eixo_detail'),
    path('acao/<int:acao_id>/atualizar/', views.atualizar_evolucao, name='atualizar_evolucao'),
]
