from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    genero = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)
    diretor = models.CharField(max_length=100)
    elenco = models.CharField(max_length=200)
    data_lancamento = models.DateTimeField('data de lançamento')
    avaliacao_media = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    avaliacao_imdb = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)


class Comentario(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.CharField(max_length=200, blank=True)
    avaliacao = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    data_criacao = models.DateTimeField('data de publicacao')

    class Meta:
        unique_together = ['filme', 'user']


class Seguidor(models.Model):
    seguidor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguidor')
    seguido = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seguido')
    data_follow = models.DateTimeField('data de follow')

    class Meta:
        unique_together = ['seguidor', 'seguido']


class Notificacao(models.Model):
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='destinatario')
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remetente')
    visto = models.BooleanField(default=False)
    comentario = models.ForeignKey(Comentario, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('comentario', 'destinatario', 'remetente')
