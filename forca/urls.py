from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.AlunoRegisterView.as_view(), name='register'),

    # Rotas do Jogo
    path('tema/<int:pk>/jogar/', views.JogarPorTemaView.as_view(), name='jogar-por-tema'),
    path('palavra/<int:pk>/jogar/', views.JogarPalavraView.as_view(), name='jogar-palavra'),

    # Rotas do Professor
    path('professor/temas/', views.TemaGerenciarView.as_view(), name='tema-gerenciar'),
    path('professor/tema/criar/', views.TemaCreateView.as_view(), name='tema-create'),
    path('professor/tema/<int:pk>/editar/', views.editar, name='editar-tema'),
    path('professor/tema/<int:pk>/deletar/', views.TemaDeleteView.as_view(), name='tema-delete'),
    path('professor/tema/<int:pk>/pdf/', views.TemaPDFView.as_view(), name='tema-pdf'),
    path('professor/relatorio/', views.RelatorioJogadasView.as_view(), name='relatorio-jogadas'),

    # Rotas da API (chamadas por JavaScript)
    path('api/palavra/<int:pk>/', views.ApiPalavraView.as_view(), name='api-palavra'),
    path('api/salvar_jogada/', csrf_exempt(views.SalvarJogadaView.as_view()), name='salvar-jogada'),
]