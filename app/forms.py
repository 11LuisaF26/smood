from django.forms import ModelForm
from django.db import models
from django import forms
from .models import *

class campana_publicitaria_form(ModelForm):
    class Meta():
        model = campana_publicitaria
        fields = ('nombre_campana', 'objetivo_campana', 'publico_campana','ubicacion_campana', 'presupuesto_campana', 'eficacia_camapana', 'empresa_campana', 'usuario_campana')

class empresa_form(ModelForm): 
    class Meta():
        model = empresa
        fields = ('nombre_empresa', 'estado_empresa', 'usuarios')
        
                
class red_social_form(ModelForm): 
    class Meta():
        model = red_social
        fields = ('nombre_red_social',)
        # 'cantidad_seguidores_red_social', 'cantidad_likes_red_social','cantidad_reacciones_red_social',

class escucha_form(ModelForm): 
    class Meta():
        model = escucha
        fields = ('nombre_escucha','usuario_red_social', 'fecha_inicio_red_social', 'fecha_final_red_social', 'empresa_red_social', 'campana_publicitaria_red_social', 'es_competencia', 'ubicacion_red_social', 'hashtag_red_social', 'red_social',)
        # 'cantidad_seguidores_red_social', 'cantidad_likes_red_social','cantidad_reacciones_red_social',

class ubicacion_form(ModelForm): 
    class Meta():
        model = ubicacion
        fields = ( 'nombre_ubicacion',)
        
class hashtag_form(ModelForm): 
    class Meta():
        model = hashtag
        fields = ('nombre_hastag',)

class credenciales_form(ModelForm): 
    class Meta():
        model = escucha_credencial
        fields = ('twitter_bearer_token', 'instagram_username', 'instagram_password', 'instagram_path',)

class data_red_form(ModelForm):
    class Meta():
        model = data_red
        fields = ('publicacion_id', 'publicacion_fecha','publicacion_texto','publicacion_likes','publicacion_comentarios',
        'publicacion_compartidos', 'publicacion_user' , 'is_from_hashtag' , 'data_red_escucha', 'data_red_campana','data_red_social',)


