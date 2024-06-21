from django.contrib import admin

# Register your models here.
from .models import Equipamento, Espaco
from recursos import models

# @admin.register(models.Recurso)

# class Recurso(admin.ModelAdmin):
#     list_display = ['nome', 'descricao', 'tipo', 'id',]

class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'quantTotal', 'quantDisponivel', 'id']

class EspacoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'localizacao', 'id']
# class RecursoAdmin(admin.ModelAdmin):
#     list_display = ['nome', 'descricao', 'tipo', 'id',]

# admin.site.register(Recurso, RecursoAdmin)

admin.site.register(Equipamento, EquipamentoAdmin)
admin.site.register(Espaco, EspacoAdmin)