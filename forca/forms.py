from django import forms
from django.contrib.auth.models import User
from .models import Aluno

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
