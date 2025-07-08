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
            aluno = Aluno.objects.create(user=user, nome=self.cleaned_data['nome'])
        return user

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nome', 'login_obrigatorio']

class PalavraForm(forms.ModelForm):
    class Meta:
        model = Palavra
        fields = ['texto', 'dica']
        widgets = {
            'texto': forms.TextInput(attrs={'class': 'edit-texto'}),
            'dica': forms.TextInput(attrs={'class': 'edit-dica'}),
        }

PalavraFormSet = inlineformset_factory(
    Tema,
    Palavra,
    form=PalavraForm,
    extra=1,
    can_delete=True
)