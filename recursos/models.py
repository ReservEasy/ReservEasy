from django.db import models

# Create your models here.

class Recurso(models.Model):
    nome = models.CharField(max_length=100, blank = 'False', null = 'False',)
    imagem = models.ImageField(blank = 'False', null = 'False', upload_to='pictures/%Y/%m/')
    descricao = models.CharField(max_length=100, blank = 'True', null = 'True')
    tipo = models.CharField(max_length=12, blank = 'False', null = 'False', choices=[('Equipamento', 'Equipamento'), ('Espaco', 'Espaço')])
# nós mostramos ao listar o que está armazenado no sistema (primeiro nome), é melhor deixar escrito do jeito maior ou fazer um if ao exibir (na tabela)?


    # def _str_(self):
    #    return self.nome
