# Generated by Django 3.0.8 on 2022-01-05 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20211011_1107'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Dados_pacotes_procedimentos',
        ),
        migrations.DeleteModel(
            name='Fact_atendimentos',
        ),
        migrations.DeleteModel(
            name='Fact_pacote',
        ),
        migrations.DeleteModel(
            name='Procedimentos_individuais',
        ),
    ]
