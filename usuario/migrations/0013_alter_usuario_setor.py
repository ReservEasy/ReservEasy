# Generated by Django 4.2.6 on 2024-07-28 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setor', '0001_initial'),
        ('usuario', '0012_alter_usuario_setor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='setor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usuarios', to='setor.setor'),
        ),
    ]
