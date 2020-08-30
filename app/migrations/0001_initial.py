# Generated by Django 2.1.15 on 2020-08-27 17:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='campana_publicitaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_campana', models.CharField(blank=True, max_length=100, verbose_name='Nombre')),
                ('descripcion_campana', models.CharField(blank=True, max_length=100, verbose_name='Descripcion')),
                ('objetivo_campana', models.CharField(blank=True, max_length=100, verbose_name='Objetivo')),
                ('publico_campana', models.CharField(blank=True, max_length=100, verbose_name='Publico')),
                ('ubicacion_campana', models.CharField(blank=True, max_length=100, verbose_name='Ubicacion')),
                ('presupuesto_campana', models.IntegerField(null=True, verbose_name='Presupuesto')),
                ('eficacia_camapana', models.CharField(blank=True, max_length=100, verbose_name='Eficacia')),
            ],
            options={
                'verbose_name': 'campana_publicitaria',
                'verbose_name_plural': 'campanas_publicitarias',
            },
        ),
        migrations.CreateModel(
            name='empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit_empresa', models.IntegerField(null=True, unique=True, verbose_name='NIT')),
                ('nombre_empresa', models.CharField(blank=True, max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
            },
        ),
        migrations.CreateModel(
            name='estado_empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_nombre_empresa', models.CharField(blank=True, max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'estado_empresa',
                'verbose_name_plural': 'estado_empresas',
            },
        ),
        migrations.CreateModel(
            name='hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_hastag', models.CharField(blank=True, max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'hashtag',
                'verbose_name_plural': 'hashtags',
            },
        ),
        migrations.CreateModel(
            name='red_social',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_escucha', models.CharField(blank=True, max_length=100, verbose_name='NombreEscucha')),
                ('nombre_red_social', models.CharField(blank=True, max_length=100, verbose_name='Nombre')),
                ('usuario_red_social', models.CharField(blank=True, max_length=100, verbose_name='Usuario')),
                ('fecha_inicio_red_social', models.DateField(verbose_name='Fecha de Inicio')),
                ('fecha_final_red_social', models.DateField(verbose_name='Fecha Final')),
                ('campana_publicitaria_red_social', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.campana_publicitaria')),
                ('empresa_red_social', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa')),
                ('hashtag_red_social', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.hashtag')),
            ],
            options={
                'verbose_name': 'red_social',
                'verbose_name_plural': 'redes_sociales',
            },
        ),
        migrations.CreateModel(
            name='ubicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_ubicacion', models.CharField(blank=True, max_length=100, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'ubicacion',
                'verbose_name_plural': 'ubicaciones',
            },
        ),
        migrations.AddField(
            model_name='red_social',
            name='ubicacion_red_social',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ubicacion'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='estado_empresa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.estado_empresa'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='usuarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='campana_publicitaria',
            name='empresa_campana',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.empresa'),
        ),
        migrations.AddField(
            model_name='campana_publicitaria',
            name='usuario_campana',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
