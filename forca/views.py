import random
import json
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
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
from .forms import UserRegisterForm, TemaForm, PalavraForm, PalavraFormSet, RelatorioForm
from datetime import timedelta
from django.http import HttpResponse


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
    form_class = TemaForm
    template_name = 'forca/tema_form.html'
    success_url = reverse_lazy('tema-gerenciar')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset_palavras'] = PalavraFormSet(self.request.POST, prefix='palavras')
        else:
            data['formset_palavras'] = PalavraFormSet(queryset=Palavra.objects.none(), prefix='palavras')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset_palavras']

        if form.is_valid() and formset.is_valid():
            form.instance.criado_por = self.request.user
            # Primeiro, salva o objeto Tema para obter um ID
            self.object = form.save()

            # Associa o formset ao novo tema e salva as palavras
            formset.instance = self.object
            instances = formset.save(commit=False)
            for instance in instances:
                instance.criado_por = self.request.user
                instance.save()
            formset.save_m2m()

            return redirect(self.get_success_url())
        else:
            # Se houver erros, renderiza o formulário novamente com as mensagens de erro
            return self.render_to_response(self.get_context_data(form=form))

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

class JogarPorTemaView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        tema = get_object_or_404(Tema, pk=pk)

        if tema.login_obrigatorio and not request.user.is_authenticated:
            return redirect('login')

        # Usamos .order_by('?') para pegar uma palavra aleatória diretamente do banco de dados
        palavra = Palavra.objects.filter(tema=tema).order_by('?').first()

        if palavra:
            return redirect('jogar-palavra', palavra_id=palavra.pk)
        else:
            # Esta parte pode ser melhorada para mostrar uma mensagem de erro mais amigável
            # return render(request, 'forca/erro.html', {'mensagem': 'Nenhuma palavra disponível.'})
            return redirect('home') # Por agora, redireciona para a home se não houver palavras


class JogarPalavraView(View):
    def get(self, request, pk):
        palavra = get_object_or_404(Palavra, pk=pk)
        return render(request, 'forca/jogo.html', {
            'palavra_id': palavra.pk,
            'tema': palavra.tema.nome,
            'dica': palavra.dica,
        })

class ApiPalavraView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        palavra = get_object_or_404(Palavra, pk=pk)
        return JsonResponse({'palavra': palavra.texto})

class SalvarJogadaView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            palavra_id = data.get('palavra_id')
            acertou = data.get('acertou')
            erros = data.get('erros')

            palavra = get_object_or_404(Palavra, pk=palavra_id)

            aluno = request.user if request.user.is_authenticated else None

            Jogada.objects.create(
                aluno=aluno,
                palavra=palavra,
                acertou=acertou,
                erros=erros
            )
            return JsonResponse({'status': 'ok'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class ProfessorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'professor/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
            data['formset_palavras'] = PalavraFormSet(self.request.POST, instance=self.object, prefix='palavras')
        else:
            data['formset_palavras'] = PalavraFormSet(instance=self.object, prefix='palavras')
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset_palavras']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            # Adicionar o 'criado_por' para novas palavras
            for form_palavra in formset:
                if form_palavra.instance.pk is None and form_palavra.cleaned_data:
                    form_palavra.instance.criado_por = self.request.user
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class TemaGerenciarView(LoginRequiredMixin, ListView):
    model = Tema
    template_name = 'forca/tema_gerenciar.html'
    context_object_name = 'temas'

    def get_queryset(self):
        return Tema.objects.filter(criado_por=self.request.user)


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
        return Palavra.objects.filter(tema_id=tema_pk, criado_por=self.request.user)

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
    """
    View para editar um tema e as suas palavras, com depuração detalhada.
    """
    tema = get_object_or_404(Tema, pk=pk, criado_por=request.user)

    if request.method == 'POST':
        # Esta secção é executada quando clica em "Salvar alterações"
        print("\n--- INÍCIO DA DEPURACÃO DO POST ---")
        form_tema = TemaForm(request.POST, instance=tema)
        formset_palavras = PalavraFormSet(request.POST, instance=tema, prefix='palavras')

        form_tema_valid = form_tema.is_valid()
        formset_palavras_valid = formset_palavras.is_valid()

        print(f"[DEBUG] O formulário do tema é válido? -> {form_tema_valid}")
        print(f"[DEBUG] O formulário das palavras é válido? -> {formset_palavras_valid}")

        # Se o formset das palavras não for válido, vamos ver exatamente porquê
        if not formset_palavras_valid:
            print("[!!!] ERROS ENCONTRADOS NO FORMULÁRIO DAS PALAVRAS:")
            for i, form in enumerate(formset_palavras):
                if form.errors:
                    print(f"  - Erros na Palavra #{i + 1}: {form.errors.as_json()}")

            if formset_palavras.non_form_errors():
                print(f"  - Erros Gerais do Formset: {formset_palavras.non_form_errors()}")

        if form_tema_valid and formset_palavras_valid:
            print("[DEBUG] Sucesso! Ambos os formulários são válidos. A salvar no banco de dados...")
            form_tema.save()
            formset_palavras.save()  # O método .save() já trata de criar, editar e apagar.
            print("[DEBUG] Salvo com sucesso! A redirecionar...")
            return redirect('tema-gerenciar')
        else:
            print("[!!!] FALHA NA VALIDAÇÃO. A página será recarregada, descartando as alterações.")
            print("--- FIM DA DEPURACÃO DO POST ---\n")

    else:  # GET request
        form_tema = TemaForm(instance=tema)
        formset_palavras = PalavraFormSet(instance=tema, prefix='palavras')

    # O template é renderizado aqui, tanto para o acesso inicial (GET) como em caso de erro no POST
    return render(request, 'forca/editar.html', {
        'form_tema': form_tema,
        'formset_palavras': formset_palavras
    })

class ProfessorListView(ListView):
    model = Professor
    template_name = 'forca/professor_list.html'
    context_object_name = 'professores'


class TemaPorProfessorListView(ListView):
    model = Tema
    template_name = 'forca/tema_por_professor_list.html'
    context_object_name = 'temas'

    def get_queryset(self):
        professor_id = self.kwargs['professor_id']
        # Assumindo que o modelo 'Tema' tem um campo 'criado_por' que é um ForeignKey para User (Professor)
        return Tema.objects.filter(criado_por__id=professor_id)

class TemaPDFView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Gera uma folha de atividade em PDF para um tema, incluindo uma página
    de gabarito para o professor. VERSÃO DE CORREÇÃO.
    """

    def test_func(self):
        # Apenas professores podem aceder a isto
        return self.request.user.is_staff

    def get(self, request, *args, **kwargs):
        # 1. Obter os dados do banco de dados
        pk = self.kwargs.get('pk')
        tema = get_object_or_404(Tema, pk=pk, criado_por=request.user)
        palavras = tema.palavras.all()

        # 2. Preparar o "arquivo" PDF na memória
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter  # width=612, height=792

        # ==================================================================
        # PARTE 1: DESENHAR A FOLHA DE ATIVIDADES PARA O ALUNO
        # ==================================================================

        # Desenhar cabeçalho da primeira página
        p.setFont("Helvetica", 9)
        p.drawString(inch, height - 0.5 * inch, "Escola: _________________________________________")
        p.drawString(width / 2, height - 0.5 * inch, "Aluno(a): _______________________________________")
        p.line(inch, height - 0.7 * inch, width - inch, height - 0.7 * inch)

        # Desenhar título da atividade
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(width / 2.0, height - 1.2 * inch, f"Jogo da Forca: {tema.nome}")
        p.setFont("Helvetica", 12)
        p.drawCentredString(width / 2.0, height - 1.6 * inch, "Complete os espaços com as letras corretas!")

        # Posição Y inicial (vertical), começando de cima para baixo
        y_position = height - 2.5 * inch

        # Loop para desenhar cada palavra na folha de atividades
        for i, palavra in enumerate(palavras):
            # Verificar se precisamos de uma nova página
            if y_position < 2.5 * inch:
                p.showPage()  # Termina a página atual e começa uma nova
                # Desenhar o cabeçalho novamente na nova página
                p.setFont("Helvetica", 9)
                p.drawString(inch, height - 0.5 * inch, "Escola: _________________________________________")
                p.drawString(width / 2, height - 0.5 * inch, "Aluno(a): _______________________________________")
                p.line(inch, height - 0.7 * inch, width - inch, height - 0.7 * inch)
                y_position = height - 1.2 * inch  # Reiniciar a posição Y no topo

            # Desenhar o número da palavra e a dica
            p.setFont("Helvetica-Bold", 14)
            p.drawString(inch, y_position, f"{i + 1}. Palavra:")
            if palavra.dica:
                p.setFont("Helvetica-Oblique", 11)
                p.drawString(inch * 3, y_position, f"(Dica: {palavra.dica})")

            y_position -= 0.5 * inch  # Mover para baixo para os quadrados

            # Desenhar os quadrados para as letras
            letter_box_size = 0.3 * inch
            start_x = inch
            for letra in palavra.texto:
                if letra == ' ':
                    start_x += letter_box_size + 5
                else:
                    p.rect(start_x, y_position, letter_box_size, letter_box_size)
                    start_x += letter_box_size + 5

            y_position -= 1.2 * inch  # Mover para baixo para a próxima palavra

        # ==================================================================
        # PARTE 2: DESENHAR A PÁGINA DE GABARITO (RESPOSTAS)
        # ==================================================================

        # Forçar o início de uma nova página para o gabarito
        p.showPage()

        # Desenhar cabeçalho da página de gabarito
        p.setFont("Helvetica", 9)
        p.drawString(inch, height - 0.5 * inch, "Escola: _________________________________________")
        p.drawString(width / 2, height - 0.5 * inch, "Aluno(a): _______________________________________")
        p.line(inch, height - 0.7 * inch, width - inch, height - 0.7 * inch)

        # Desenhar título do gabarito
        p.setFont("Helvetica-Bold", 18)
        p.drawCentredString(width / 2.0, height - 1.2 * inch, "GABARITO - Respostas")
        p.setFont("Helvetica-Oblique", 12)
        p.drawCentredString(width / 2.0, height - 1.5 * inch, f"(Tema: {tema.nome})")

        # --- A LÓGICA DE DESENHO DO GABARITO COMEÇA AQUI ---
        # REINICIAR a posição Y para o conteúdo do gabarito
        y_position = height - 2.5 * inch
        p.setFont("Helvetica", 12)

        # Loop para escrever cada resposta
        for i, palavra in enumerate(palavras):
            # Verificar se precisamos de uma nova página PARA O GABARITO
            if y_position < inch:
                p.showPage()  # Termina a página atual e começa uma nova
                # Desenhar o cabeçalho novamente
                p.setFont("Helvetica", 9)
                p.drawString(inch, height - 0.5 * inch, "Escola: _________________________________________")
                p.drawString(width / 2, height - 0.5 * inch, "Aluno(a): _______________________________________")
                p.line(inch, height - 0.7 * inch, width - inch, height - 0.7 * inch)
                p.setFont("Helvetica-Bold", 12)
                p.drawCentredString(width / 2.0, height - inch, "GABARITO (continuação)")
                y_position = height - 1.5 * inch  # Reiniciar a posição Y

            # Definir a fonte para a resposta
            p.setFont("Helvetica", 12)
            # Desenhar a resposta
            p.drawString(inch, y_position, f"{i + 1}. {palavra.texto.upper()}")
            # Mover a posição para baixo para a próxima resposta
            y_position -= 0.5 * inch

        # 3. Finalizar e salvar o PDF
        p.save()

        # 4. Enviar o PDF para o browser
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=False, filename=f'atividade_{tema.nome}.pdf')


class RelatorioJogadasView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'forca/relatorio.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = RelatorioForm(self.request.GET or None)
        form.fields['tema'].queryset = Tema.objects.filter(criado_por=self.request.user).order_by('nome')

        context['form'] = form
        jogadas = []

        if form.is_valid():
            tema = form.cleaned_data.get('tema')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')

            query_jogadas = Jogada.objects.filter(palavra__tema__criado_por=self.request.user)

            if tema:
                query_jogadas = query_jogadas.filter(palavra__tema=tema)
            if data_inicio:
                # CORREÇÃO AQUI: de 'criado_em__gte' para 'data__gte'
                query_jogadas = query_jogadas.filter(data__gte=data_inicio)
            if data_fim:
                # CORREÇÃO AQUI: de 'criado_em__lte' para 'data__lte'
                query_jogadas = query_jogadas.filter(data__lte=data_fim + timedelta(days=1))

            # CORREÇÃO AQUI: de '-criado_em' para '-data'
            jogadas = query_jogadas.select_related('aluno', 'palavra__tema').order_by('-data')

        context['jogadas'] = jogadas
        return context
