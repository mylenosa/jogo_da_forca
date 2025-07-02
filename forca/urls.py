from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('temas/', views.TemaListView.as_view(), name='tema-list'),
    path('temas/novo/', views.TemaCreateView.as_view(), name='tema-create'),
    path('palavras/novo/', views.PalavraCreateView.as_view(), name='palavra-create'),
    path('cadastro/', views.AlunoRegisterView.as_view(), name='aluno-register'),
    path('jogar/', views.JogarEscolherTemaView.as_view(), name='escolher-tema'),
    path('jogar/tema/<int:pk>/', views.jogar_por_tema, name='jogar-tema'),
    path('jogar/palavra/<int:pk>/', views.JogarPalavraView.as_view(), name='jogar-palavra'),
    path('api/palavra/<int:pk>/', views.api_palavra, name='api-palavra'),
    path('api/salvar_jogada/', views.salvar_jogada, name='salvar-jogada'),
    # URLs futuras para jogo, PDF, relatório, etc.
]
