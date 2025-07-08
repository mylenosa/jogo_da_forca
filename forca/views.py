import random
import json
from django.db import models
from django.shortcuts import redirect, get_object_or_404, render
from django.forms import inlineformset_factory
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from .models import Tema, Palavra, Jogada, Professor
from .forms import UserRegisterForm, TemaForm, PalavraForm

PalavraFormSet = inlineformset_factory(
    Tema, Palavra,
    fields=['texto', 'dica'],
    extra=0,  # zero linhas extras
    can_delete=True
)

class HomeView(TemplateView):
    template_name = 'forca/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        temas = Tema.objects.all().select_related('criado_por')

        if query:
            temas = temas.filter(
                models.Q(nome__icontains=query) |
                models.Q(criado_por__username__icontains=query)
            )

        context['temas'] = temas
        context['q'] = query or ''
        return context

class TemaListView(ListView):
    model = Tema
    paginate_by = 10
    template_name = 'tema_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(
                Q(nome__icontains=q) | Q(criado_por__username__icontains=q)
            )
        return queryset.order_by('nome')

class ProfessorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # professores são staff

class TemaCreateView(LoginRequiredMixin, CreateView):
    model = Tema
    fields = ['nome', 'login_obrigatorio']
    template_name = 'forca/tema_form.html'

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tema-gerenciar')

class PalavraCreateView(LoginRequiredMixin, CreateView):
    model = Palavra
    fields = ['texto']
    template_name = 'forca/palavra_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.tema = get_object_or_404(Tema, pk=kwargs['tema_pk'])
        if self.tema.login_obrigatorio and not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = self.tema
        return context

    def form_valid(self, form):
        form.instance.tema = self.tema
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('palavra-list', args=[self.tema.pk])

class AlunoRegisterView(FormView):
    template_name = 'forca/register.html'
    form_class = UserRegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def jogar_por_tema(request, pk):
    tema = get_object_or_404(Tema, pk=pk)

    # VERIFICAÇÃO IMPORTANTE
    if tema.login_obrigatorio and not request.user.is_authenticated:
        return redirect('login')  # ou exibir mensagem personalizada

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

class ProfessorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'professor/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Busca todos os temas criados pelo professor logado
        context['temas'] = self.request.user.temas.all()
        return context

class TemaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tema
    form_class = TemaForm
    template_name = 'forca/editar.html'
    success_url = reverse_lazy('tema-gerenciar')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['formset_palavras'] = PalavraFormSet(self.request.POST, instance=self.object)
        else:
            data['formset_palavras'] = PalavraFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset_palavras']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class TemaGerenciarView(LoginRequiredMixin, ListView):
    model = Tema
    template_name = 'forca/tema_gerenciar.html'
    context_object_name = 'temas'

    def get_queryset(self):
        # Apenas os temas criados pelo professor logado
        return Tema.objects.filter(criado_por=self.request.user)
class TemaUpdateView(UpdateView):
    model = Tema
    form_class = TemaForm
    template_name = 'forca/editar.html'  # <-- aqui você escolhe o template
    success_url = reverse_lazy('tema-gerenciar')

class TemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tema
    template_name = 'forca/confirm_delete.html'

    def get_success_url(self):
        return reverse('tema-gerenciar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto_tipo'] = 'tema'
        return context

class PalavraListView(LoginRequiredMixin, ListView):
    model = Palavra
    template_name = 'forca/palavra_list.html'
    context_object_name = 'palavras'

    def get_queryset(self):
        self.tema = get_object_or_404(Tema, pk=self.kwargs['tema_pk'])
        # Se o tema exigir login, só mostra para usuários autenticados
        if self.tema.login_obrigatorio and not self.request.user.is_authenticated:
            return Palavra.objects.none()
        return Palavra.objects.filter(tema=self.tema)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tema'] = self.tema
        return context

class PalavraUpdateView(LoginRequiredMixin, UpdateView):
    model = Palavra
    form_class = PalavraForm
    template_name = 'forca/palavra_form.html'

    def get_queryset(self):
        tema_pk = self.kwargs['tema_pk']
        return Palavra.objects.filter(tema_id=tema_pk)

    def get_success_url(self):
        return reverse('editar-tema', kwargs={'pk': self.kwargs['tema_pk']})

class PalavraDeleteView(LoginRequiredMixin, DeleteView):
    model = Palavra
    template_name = 'forca/confirm_delete.html'

    def get_success_url(self):
        return reverse('palavra-list', kwargs={'tema_pk': self.object.tema.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objeto_tipo'] = 'palavra'
        return context

def editar(request, pk):
    tema = get_object_or_404(Tema, pk=pk)
    form_tema = TemaForm(request.POST or None, instance=tema)
    formset_palavras = PalavraFormSet(request.POST or None, instance=tema)

    if request.method == 'POST':
        if form_tema.is_valid() and formset_palavras.is_valid():
            form_tema.save()
            formset_palavras.save()
            return redirect('tema-gerenciar')

    print(form_tema)

    return render(request, 'forca/editar.html', {
        'form_tema': form_tema,
        'formset_palavras': formset_palavras
    })


class ProfessorListView(ListView):
    model = Professor
    template_name = 'forca/professor_list.html'  # crie esse template ou ajuste o nome
    context_object_name = 'professores'

class TemaPorProfessorListView(ListView):
    model = Tema
    template_name = 'forca/tema_por_professor_list.html'  # ajuste conforme seu template
    context_object_name = 'temas'

    def get_queryset(self):
        professor_id = self.kwargs['professor_id']
        return Tema.objects.filter(professor__id=professor_id)