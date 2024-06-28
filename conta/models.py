from django.db import models
from django.contrib.auth.models import User

class Usuario(User):
    matricula = models.CharField(max_length=15, unique=True)
    telefone = models.CharField(max_length=15)
    turma = models.CharField(max_length=4, blank=True, null=True)
    data_nascimento = models.DateField()
    cargo = models.CharField(max_length=100, default='não identificado', blank=True, null=True)  
    status = models.CharField(max_length=50, default='Ativo', blank=True, null=True)
