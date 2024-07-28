from django.db import models
from setor.models import Setor
# Create your models here.

class Recurso(models.Model):
    nome = models.CharField(max_length=100, blank = 'False', null = 'False')
    imagem = models.ImageField(blank = 'False', null = 'False', upload_to='pictures/%Y/%m/')
    descricao = models.CharField(max_length=100, blank = 'True', null = 'True')

    class Meta: #a classe Recurso é abstrata e nao vai ter uma tabela para ela, apenas um modelo
        abstract = True
    
    #descobrir qual tipo de classe a instancia pertence 
    def get_tipo(self):
        return self.__class__.__name__

#herdando de recurso
class Equipamento(Recurso):
    quantTotal = models.IntegerField()
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name="equipamentos")
    def __str__(self):
        return self.nome

class Espaco(Recurso):
    localizacao = models.CharField(max_length=100)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name="espacos")
    def __str__(self):
        return self.nome
