# Generated by Django 4.2.6 on 2024-08-19 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0004_reserva_situacao_alter_reserva_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='situacao',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
