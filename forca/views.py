import random
import json
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.utils.html import escape
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Tema, Palavra, Jogada
from .forms import UserRegisterForm

class HomeView(TemplateView):
    template_name = 'forca/home.html'

class TemaListView(ListView):
    model = Tema
    template_name = 'forca/tema_list.html'
    context_object_name = 'temas'

class ProfessorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # professores são staff

class TemaCreateView(ProfessorRequiredMixin, CreateView):
    model = Tema
    fields = ['nome']
    template_name = 'forca/tema_form.html'
    success_url = reverse_lazy('tema-list')

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

class PalavraCreateView(ProfessorRequiredMixin, CreateView):
    model = Palavra
    fields = ['tema', 'texto', 'dica', 'texto_extra']
    template_name = 'forca/palavra_form.html'
    success_url = reverse_lazy('tema-list')

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

class AlunoRegisterView(FormView):
    template_name = 'forca/register.html'
    form_class = UserRegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class JogarEscolherTemaView(ListView):
    model = Tema
    template_name = 'forca/escolher_tema.html'
    context_object_name = 'temas'

def jogar_por_tema(request, pk):
    tema = get_object_or_404(Tema, pk=pk)
    palavras = Palavra.objects.filter(tema=tema)
    if palavras.exists():
        palavra = random.choice(palavras)
        return redirect('jogar-palavra', palavra.pk)
    else:
        return render(request, 'forca/erro.html', {
            'mensagem': 'Nenhuma palavra disponível para este tema.'
        })

class JogarPalavraView(View):
    def get(self, request, pk):
        palavra = get_object_or_404(Palavra, pk=pk)
        return render(request, 'forca/jogo.html', {
            'palavra_id': palavra.pk,
            'tema': palavra.tema.nome,
            'dica': palavra.dica,
        })

@csrf_exempt
def api_palavra(request, pk):
    palavra = get_object_or_404(Palavra, pk=pk)
    return JsonResponse({'palavra': palavra.texto})

@require_POST
def salvar_jogada(request):
    data = json.loads(request.body)
    palavra_id = data.get('palavra_id')
    acertou = data.get('acertou')
    erros = data.get('erros')

    palavra = get_object_or_404(Palavra, pk=palavra_id)

    aluno = None
    if request.user.is_authenticated:
        aluno = request.user

    jogada = Jogada.objects.create(
        aluno=aluno,
        palavra=palavra,
        acertou=acertou,
        erros=erros
    )
    return JsonResponse({'status': 'ok'})

User = get_user_model()

class ProfessorListView(ListView):
    model = User
    template_name = 'forca/professor_list.html'
    context_object_name = 'professores'

    def get_queryset(self):
        return User.objects.filter(is_staff=True, temas__isnull=False).distinct()

class TemaPorProfessorListView(ListView):
    model = Tema
    template_name = 'forca/tema_por_professor.html'
    context_object_name = 'temas'

    def get_queryset(self):
        professor_id = self.kwargs['professor_id']
        return Tema.objects.filter(criado_por__id=professor_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['professor'] = get_object_or_404(User, id=self.kwargs['professor_id'])
        return context

