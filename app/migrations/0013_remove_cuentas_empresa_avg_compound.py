# Generated by Django 2.1.15 on 2022-06-07 02:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_cuentas_empresa_avg_compound'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentas_empresa',
            name='avg_compound',
        ),
    ]
