# Generated by Django 4.2.6 on 2024-02-27 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recursos', '0005_alter_recurso_imagem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurso',
            name='dataAquisicao',
        ),
    ]