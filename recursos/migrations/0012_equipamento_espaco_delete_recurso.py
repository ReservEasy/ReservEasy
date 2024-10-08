# Generated by Django 4.2.6 on 2024-06-05 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursos', '0011_recurso_quantidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank='False', max_length=100, null='False')),
                ('imagem', models.ImageField(blank='False', null='False', upload_to='pictures/%Y/%m/')),
                ('descricao', models.CharField(blank='True', max_length=100, null='True')),
                ('quantTotal', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Espaco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank='False', max_length=100, null='False')),
                ('imagem', models.ImageField(blank='False', null='False', upload_to='pictures/%Y/%m/')),
                ('descricao', models.CharField(blank='True', max_length=100, null='True')),
                ('localizacao', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Recurso',
        ),
    ]
