# Generated by Django 4.2.6 on 2024-05-14 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conta', '0004_alter_usuario_telefone_alter_usuario_turma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='telefone',
            field=models.CharField(default='não', max_length=15),
        ),
    ]
