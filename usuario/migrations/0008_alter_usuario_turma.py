# Generated by Django 4.2.6 on 2024-07-01 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_alter_usuario_cargo_alter_usuario_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='turma',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
