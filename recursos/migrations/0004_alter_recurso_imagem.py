# Generated by Django 4.2.6 on 2024-02-25 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recursos', '0003_alter_recurso_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recurso',
            name='imagem',
            field=models.ImageField(blank=True, upload_to='pictures/%Y/%m/'),
        ),
    ]
