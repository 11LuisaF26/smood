from django.forms import ModelForm
from django.db import models
from django import forms
from .models import *

class campana_publicitaria_form(ModelForm):
    class Meta():
        model = campana_publicitaria
        fields = ('nombre_campana', 'descripcion_campana', 'objetivo_campana', 'publico_campana','ubicacion_campana', 'presupuesto_campana', 'eficacia_camapana', 'empresa_campana', 'usuario_campana')

class empresa_form(ModelForm): 
    class Meta():
        model = empresa
        fields = ('nit_empresa', 'nombre_empresa', 'estado_empresa', 'usuarios')
        
                
class red_social_form(ModelForm): 
    class Meta():
        model = red_social
        fields = ('nombre_escucha','nombre_red_social','usuario_red_social','fecha_inicio_red_social','fecha_final_red_social','empresa_red_social','campana_publicitaria_red_social', 'ubicacion_red_social','hashtag_red_social', 
        # 'cantidad_seguidores_red_social', 'cantidad_likes_red_social','cantidad_reacciones_red_social',
        )
        
class ubicacion_form(ModelForm): 
    class Meta():
        model = ubicacion
        fields = ( 'nombre_ubicacion',)



class hashtag_form(ModelForm): 
    class Meta():
        model = hashtag
        fields = ('nombre_hastag',)
