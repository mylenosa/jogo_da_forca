from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    # Tema
    path('temas/novo/', views.TemaCreateView.as_view(), name='tema-create'),
#    path('tema/<int:pk>/editar/', views.TemaUpdateView.as_view(), name='tema-update'),
    path('tema/<int:pk>/excluir/', views.TemaDeleteView.as_view(), name='tema-delete'),

    # Gerenciamento do professor
    path('professor/temas/', views.TemaGerenciarView.as_view(), name='tema-gerenciar'),
    path('professor/tema/<int:pk>/editar/', views.editar, name='editar-tema'),

    # Palavra (por tema)
    path('tema/<int:tema_pk>/palavras/', views.PalavraListView.as_view(), name='palavra-list'),
    path('tema/<int:tema_pk>/palavras/nova/', views.PalavraCreateView.as_view(), name='palavra-create'),
#    path('professor/tema/<int:tema_pk>/editar/', views.TemaUpdateView.as_view(), name='editar-tema'),
    path('tema/<int:tema_pk>/palavra/<int:pk>/editar/', views.PalavraUpdateView.as_view(), name='palavra-update'),
    path('tema/<int:tema_pk>/palavra/<int:pk>/excluir/', views.PalavraDeleteView.as_view(), name='palavra-delete'),

    # Aluno
    path('cadastro/', views.AlunoRegisterView.as_view(), name='aluno-register'),

    # Jogo
    path('jogar/<int:pk>/', views.jogar_por_tema, name='jogar'),
    path('jogar/tema/<int:pk>/', views.jogar_por_tema, name='jogar-tema'),
    path('jogar/palavra/<int:pk>/', views.JogarPalavraView.as_view(), name='jogar-palavra'),

    # API
    path('api/palavra/<int:pk>/', views.api_palavra, name='api-palavra'),
    path('api/salvar_jogada/', views.salvar_jogada, name='salvar-jogada'),

    # Professores e temas por professor
    path('professores/', views.ProfessorListView.as_view(), name='professor_list'),
    path('professor/<int:professor_id>/temas/', views.TemaPorProfessorListView.as_view(), name='tema_por_professor'),
    path('professor/tema/<int:pk>/pdf/', views.TemaPDFView.as_view(), name='tema-pdf'),
    path('professor/relatorio/', views.RelatorioJogadasView.as_view(), name='relatorio-jogadas'),

]
