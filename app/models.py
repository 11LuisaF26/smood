# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
from django.db import models
from django.contrib.auth.models import User , Group
from django import forms

# Create your models here.
class estado_empresa(models.Model):
    estado_nombre_empresa = models.CharField(blank=True, max_length=100, verbose_name='Nombre')

    class Meta():
        verbose_name = "estado_empresa"
        verbose_name_plural = "estado_empresas"

    def __str__(self):
        return self.estado_nombre_empresa

class empresa(models.Model):
    nit_empresa = models.CharField(null=True, unique=True, max_length=100, verbose_name='NIT')
    nombre_empresa = models.CharField(blank=True, max_length=100, verbose_name='Nombre')
    estado_empresa = models.ForeignKey(estado_empresa, on_delete=models.CASCADE, null=True)
    usuarios = models.ManyToManyField(User)

    class Meta():
        verbose_name = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self):
        return self.nombre_empresa

class ubicacion(models.Model):
    nombre_ubicacion = models.CharField(blank=True, max_length=100, verbose_name='Nombre')    
    class Meta():
        verbose_name = "ubicacion"
        verbose_name_plural = "ubicaciones"
    def __str__(self):
        return self.nombre_ubicacion       
        
class campana_publicitaria(models.Model):
    nombre_campana = models.CharField(blank=True, max_length=100, verbose_name='Nombre')
    descripcion_campana = models.CharField(blank=True, max_length=100, verbose_name='Descripcion')
    objetivo_campana = models.CharField(blank=True, max_length=100, verbose_name='Objetivo')
    publico_campana = models.CharField(blank=True, max_length=100, verbose_name='Publico')
    ubicacion_campana = models.ForeignKey(ubicacion, on_delete=models.CASCADE, null=True)
    presupuesto_campana = models.IntegerField(null=True, verbose_name='Presupuesto')
    eficacia_camapana = models.CharField(blank=True, max_length=100, verbose_name='Eficacia')
    empresa_campana = models.ForeignKey(empresa, on_delete=models.CASCADE, null=True)
    usuario_campana = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta():
        verbose_name = "campana_publicitaria"
        verbose_name_plural = "campanas_publicitarias"

    def __str__(self):  
        return self.nombre_campana     

class hashtag(models.Model):
    nombre_hastag = models.CharField(blank=True, max_length=100, verbose_name='Nombre')
    

    class Meta():
        verbose_name = "hashtag"
        verbose_name_plural = "hashtags"

    def __str__(self):
        return self.nombre_hastag

class red_social(models.Model):
    nombre_red_social = models.CharField(blank=True, max_length=100, verbose_name='Nombre')

    class Meta():
        verbose_name = "red_social"
        verbose_name_plural = "redes_sociales"

    def __str__(self):
        return self.nombre_red_social

    # cantidad_seguidores_red_social = models.IntegerField(null=True, verbose_name='Cantidad de seguidores')
    # cantidad_likes_red_social = models.IntegerField(null=True, verbose_name='Cantidad de Likes')
    # cantidad_reacciones_red_social = models.IntegerField(null=True, verbose_name='Cantidad de reacciones')

class escucha_credencial(models.Model):
    twitter_bearer_token = models.CharField(max_length=300, verbose_name='Bearer token')
    instagram_username = models.CharField(max_length=50, verbose_name='Instagram username')
    instagram_password = models.CharField(max_length=50, verbose_name='Instagram Password')
    instagram_path = models.CharField(max_length=50, verbose_name='Instagram Path')

    class Meta():
        verbose_name = "escucha_credenciales"
        verbose_name_plural = "escuchas_credenciales"

    def __str__(self):
        return self.instagram_username

class escucha(models.Model):
    nombre_escucha = models.CharField(blank=True, max_length=100, verbose_name='NombreEscucha')
    usuario_red_social = models.CharField(blank=True, max_length=100, verbose_name='Usuario')
    fecha_inicio_red_social = models.DateField(auto_now=False, auto_now_add=False,verbose_name='Fecha de Inicio')
    fecha_final_red_social = models.DateField(auto_now=False, auto_now_add=False,verbose_name='Fecha Final')    
    empresa_red_social = models.ForeignKey(empresa, on_delete=models.CASCADE, null=True)
    campana_publicitaria_red_social = models.ForeignKey(campana_publicitaria, on_delete=models.CASCADE, null=True)
    credenciales = models.ForeignKey(escucha_credencial, on_delete=models.CASCADE, null=True)
    es_competencia = models.BooleanField()
    ubicacion_red_social = models.ManyToManyField(ubicacion)
    hashtag_red_social = models.ManyToManyField(hashtag)
    red_social = models.ManyToManyField(red_social)

    class Meta():
        verbose_name = "escucha"
        verbose_name_plural = "Escuchas"

    def __str__(self):
        return self.nombre_escucha

class data_red(models.Model):
    publicacion_id = models.CharField(null=True, max_length=30, verbose_name='Id')
    publicacion_fecha = models.CharField(null=True, blank=True, max_length=60, verbose_name='Fecha')
    publicacion_texto = models.CharField(null=True, blank=True, max_length=300, verbose_name='Text')
    publicacion_likes = models.IntegerField(null=True, verbose_name='Likes')
    publicacion_comentarios = models.IntegerField(null=True, verbose_name='Comentarios')
    publicacion_compartidos = models.IntegerField(null=True, verbose_name='Veces compartido')
    publicacion_user = models.CharField(null=True, blank=True, max_length=30, verbose_name='User')
    is_from_hashtag = models.BooleanField(default=False)
    data_red_escucha = models.ForeignKey(escucha, on_delete=models.CASCADE, null=True)
    data_red_campana = models.ForeignKey(campana_publicitaria, on_delete=models.CASCADE, null=True) 
    data_red_social = models.ForeignKey(red_social, on_delete=models.CASCADE, null=True) 
    
    class Meta():
        verbose_name = "data_red"
        verbose_name_plural = "data_redes"

    def __str__(self):
        return self.publicacion_id

class cuentas_empresa(models.Model):
    identifier = models.CharField(null=True, max_length=60, verbose_name='Identificador')
    username = models.CharField(null=True, max_length=30, verbose_name='Username')
    created_at = models.CharField(null=True, max_length=30, verbose_name='Creado en')
    location = models.CharField(null=True, max_length=30, verbose_name='location')
    followers_count = models.IntegerField(null=True, verbose_name='Followers count')
    following_count = models.IntegerField(null=True, verbose_name='Following count')
    tweet_count = models.IntegerField(null=True, verbose_name='Tweet count')
    listed_count = models.IntegerField(null=True, verbose_name='Listed count')
    fullname = models.CharField(null=True, max_length=30, verbose_name='Fullname')
    profile_pic_url = models.CharField(null=True, max_length=500, verbose_name='Url foto perfil')
    data_red_escucha = models.ForeignKey(escucha, on_delete=models.CASCADE, null=True)
    data_red_campana = models.ForeignKey(campana_publicitaria, on_delete=models.CASCADE, null=True) 
    data_red_social = models.ForeignKey(red_social, on_delete=models.CASCADE, null=True) 
    
    class Meta():
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return self.username
