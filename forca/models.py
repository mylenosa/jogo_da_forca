from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Tema(models.Model):
    nome = models.CharField(max_length=100)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temas')

    def __str__(self):
        return self.nome

class Palavra(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='palavras')
    texto = models.CharField(max_length=50)
    dica = models.CharField(max_length=200, blank=True)
    texto_extra = models.TextField(blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='palavras')

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