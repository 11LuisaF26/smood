# Generated by Django 2.1.15 on 2022-06-07 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_cuentas_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentas_empresa',
            name='data_red_social',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.red_social'),
        ),
    ]