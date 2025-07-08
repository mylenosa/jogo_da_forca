from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import Aluno, Tema, Palavra

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    nome = forms.CharField(label="Nome do aluno")

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Aluno.objects.create(user=user, nome=self.cleaned_data['nome'])
        return user

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nome', 'login_obrigatorio']
        # Adicionando widgets para melhor estilização com Bootstrap
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'style': 'display: inline; width: auto;'}),
            'login_obrigatorio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ['texto', 'dica']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'edit-texto'}),
            'dica': forms.TextInput(attrs={'class': 'edit-dica'}),
        }


class RelatorioForm(forms.Form):
    tema = forms.ModelChoiceField(
        queryset=Tema.objects.all().order_by('nome'),
        required=False,
        label="Filtrar por Tema"
    )

    # DateField cria um campo de data, e o widget adiciona um calendário fácil de usar.
    data_inicio = forms.DateField(
        required=False,
        label="De",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    data_fim = forms.DateField(
        required=False,
        label="Até",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

PalavraFormSet = inlineformset_factory(
    Tema,
    Palavra,
    form=PalavraForm,
    extra=0,  # <-- MUDANÇA AQUI: de 1 para 0
    can_delete=True
)