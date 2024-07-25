from django.db import models

class Setor(models.Model):
    nome = models.CharField(max_length=100, blank = 'False', null = 'False')
    def __str__(self):
        return self.nome