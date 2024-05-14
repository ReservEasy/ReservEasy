from django.contrib import admin

# Register your models here.
from .models import Recurso

from recursos import models

# @admin.register(models.Recurso)

# class Recurso(admin.ModelAdmin):
#     list_display = ['nome', 'descricao', 'tipo', 'id',]

class RecursoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'tipo', 'id',]

admin.site.register(Recurso, RecursoAdmin)