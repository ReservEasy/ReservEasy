from django.db import models

# Create your models here.

class Recurso(models.Model):
    nome = models.CharField(max_length=100, blank = 'False', null = 'False',)
    imagem = models.ImageField(blank = 'False', null = 'False', upload_to='pictures/%Y/%m/')
    descricao = models.CharField(max_length=100, blank = 'True', null = 'True')
    # tipo = models.CharField(max_length=12, blank = 'False', null = 'False', choices=[('Equipamento', 'Equipamento'), ('Espaco', 'Espaço')])
    # quantidade = models.IntegerField(blank=False, null=False, default=1)
# nós mostramos ao listar o que está armazenado no sistema (primeiro nome), é melhor deixar escrito do jeito maior ou fazer um if ao exibir (na tabela)?


    class Meta: #a classe Recurso é abstrata e nao vai ter uma tabela para ela, apenas um modelo
        abstract = True
    
    #descobrir qual tipo de classe a instancia pertence 
    def get_tipo(self):
        return self.__class__.__name__

#herdando de recurso
class Equipamento(Recurso):
    quantTotal = models.IntegerField()
    quantDisponivel = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Atualize o valor de quantDisponivel antes de salvar
        self.quantDisponivel = self.quantTotal
        super().save(*args, **kwargs) #provisorio

class Espaco(Recurso):
    localizacao = models.CharField(max_length=100)


    # def _str_(self):
    #    return self.nome