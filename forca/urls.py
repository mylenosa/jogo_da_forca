from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('temas/', views.TemaListView.as_view(), name='tema-list'),
    path('temas/novo/', views.TemaCreateView.as_view(), name='tema-create'),
    path('palavras/novo/', views.PalavraCreateView.as_view(), name='palavra-create'),
    path('cadastro/', views.AlunoRegisterView.as_view(), name='aluno-register'),
    path('jogar/tema/<int:pk>/', views.jogar_por_tema, name='jogar-tema'),
    path('jogar/palavra/<int:pk>/', views.JogarPalavraView.as_view(), name='jogar-palavra'),
    path('api/palavra/<int:pk>/', views.api_palavra, name='api-palavra'),
    path('api/salvar_jogada/', views.salvar_jogada, name='salvar-jogada'),
    path('professores/', views.ProfessorListView.as_view(), name='professor_list'),
    path('professor/<int:professor_id>/temas/', views.TemaPorProfessorListView.as_view(), name='tema_por_professor'),
    path('jogar/', views.JogarView.as_view(), name='jogar-menu'),
    path('professor/dashboard/', views.ProfessorDashboardView.as_view(), name='professor-dashboard'),
    path('tema/<int:tema_id>/palavras/novo/', views.PalavraCreateView.as_view(), name='palavra-create-por-tema'),
    path('professor/temas/', views.TemaGerenciarView.as_view(), name='tema-gerenciar'),
    path('professor/temas/novo/', views.TemaCreateView.as_view(), name='tema-create'),
    path('professor/temas/<int:pk>/editar/', views.TemaUpdateView.as_view(), name='tema-update'),
    path('professor/temas/<int:pk>/deletar/', views.TemaDeleteView.as_view(), name='tema-delete'),
    path('professor/temas/<int:tema_pk>/palavras/', views.PalavraListView.as_view(), name='palavra-list'),
    path('professor/temas/<int:tema_pk>/palavras/novo/', views.PalavraCreateView.as_view(), name='palavra-create'),
    path('professor/palavras/<int:pk>/editar/', views.PalavraUpdateView.as_view(), name='palavra-update'),
    path('professor/palavras/<int:pk>/deletar/', views.PalavraDeleteView.as_view(), name='palavra-delete'),
    # URLs futuras para jogo, PDF, relatório, etc.
]
