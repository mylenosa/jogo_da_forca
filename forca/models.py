from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.utils import timezone

class Tema(models.Model):
    nome = models.CharField(max_length=100)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temas')
    login_obrigatorio = models.BooleanField(default=False)  # ← ESTE CAMPO

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('palavra-list', kwargs={'tema_pk': self.pk})

class Palavra(models.Model):
    texto = models.CharField(max_length=100)
    dica = models.CharField(max_length=255, blank=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='palavras')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome if self.nome else "Aluno Anônimo"

class Partida(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.SET_NULL, null=True, blank=True)
    palavra = models.ForeignKey(Palavra, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    erros = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.aluno} - {self.palavra} em {self.data.strftime('%d/%m/%Y %H:%M')}"


class Jogada(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # aluno pode ser anônimo
    palavra = models.ForeignKey(Palavra, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    acertou = models.BooleanField()
    erros = models.IntegerField()

    def __str__(self):
        return f"Jogada de {self.aluno} na palavra {self.palavra.texto} - Acertou? {self.acertou}"

class Professor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

