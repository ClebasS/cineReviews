from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.


class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genero_preferido = models.CharField(max_length=200)
    banido = models.BooleanField(default=False)


class Moderador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    genero_preferido = models.CharField(max_length=200)


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genero_preferido = models.CharField(max_length=200)
