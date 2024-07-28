# Generated by Django 4.2.6 on 2024-07-28 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setor', '0001_initial'),
        ('recursos', '0017_alter_equipamento_imagem_alter_espaco_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipamento',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipamentos', to='setor.setor'),
        ),
        migrations.AlterField(
            model_name='espaco',
            name='setor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='espacos', to='setor.setor'),
        ),
    ]
