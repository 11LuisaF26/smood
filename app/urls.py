# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views
from app import nube

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.pages, name='pages'),

    # The home page
    path('', views.index, name='home'),
    path('empresas/', views.empresas, name='empresas'),
    path('empresas/save/', views.add_empresas, name='crear_empresa'),
    path('campanas/', views.campanas_publicitarias, name='campanas_publicitarias'),
    path('campanas/save/', views.add_camapana_publicitaria, name='crear_campana'),
    path('redes/',  views.redes_sociales, name='redes_sociales'),
    path('redes/data/', views.redes_data, name='redes_data'),
    path('redes/create/', views.add_red_social, name='crear_red'),
    path('redes/save/', views.add_red_social, name='crear_red'),
    path('ubicacion/', views.add_ubicacion,  name='crear_ubicacion'),
    path('ubicacion/save/', views.ubicaciones,  name='ubicaciones'),
    path('hashtag/', views.add_hashtag, name='crear_hashtag'),
    path('hashtag/save/', views.hashtags, name='hashtags'),
    path('escucha/save/', views.add_escuchas,  name='crear_escucha'),
    path('cuentas/', views.cuentas,  name='cuentas'),
    path('acercade/', views.acerca_de, name='acerca_de'),
    path('credenciales/save/', views.add_credential, name='guardar_credenciales'),
    path('escuchas/campana/<int:campana_id>', views.escuchas_campana, name='escuchas_campana'),
    path('campanas/empresa/<int:empresa_id>', views.campanas_empresa, name='campana_empresa'),
    # path('nube/twitter', nube.cloud_gen_t, name='nube_de_palabras_twitter'),
    # path('nube/facebook', nube.cloud_gen_fb, name='nube_de_palabras_fb'),
    # path('nube/instagram', nube.cloud_gen_ig, name='nube_de_palabras_ig'),
    re_path(r'^empresas/save/(?P<id>\w+)/$', views.add_empresas, name='editar_empresa'),
    re_path(r'^empresas/delete/(?P<id>\w+)/$', views.delete_empresas, name='eliminar_empresa'),
    re_path(r'^redes/save/(?P<id>\w+)/$', views.add_red_social, name='editar_redes'),
    re_path(r'^redes/delete/(?P<id>\w+)/$', views.delete_red_social, name='eliminar_redes'),
    re_path(r'^campanas/save/(?P<id>\w+)/$', views.add_camapana_publicitaria, name='editar_campana'),
    re_path(r'^campanas/delete/(?P<id>\w+)/$', views.delete_camapana_publicitaria, name='eliminar_campana'),
    re_path(r'^escuchas/save/(?P<id>\w+)/$', views.add_escuchas, name='editar_escucha'),
    re_path(r'^escuchas/delete/(?P<id>\w+)/$', views.delete_escucha, name='eliminar_escucha'),

    #Nube de palabras
    re_path(r'^nube/twitter/(?P<id>\w+)/$', nube.cloud_gen_t, name='nube_de_palabras_twitter'),
    re_path(r'^nube/facebook/(?P<id>\w+)/$', nube.cloud_gen_fb, name='nube_de_palabras_fb'),
    re_path(r'^nube/instagram/(?P<id>\w+)/$', nube.cloud_gen_ig, name='nube_de_palabras_ig'),

    #Red de palabras
    re_path(r'^red/twitter/(?P<id>\w+)/$',  nube.red_palabras_t, name='red_de_palabras_twitter'),
    re_path(r'^red/facebook/(?P<id>\w+)/$',  nube.red_palabras_fb, name='red_de_palabras_fb'),
    re_path(r'^red/instagram/(?P<id>\w+)/$',  nube.red_palabras_ig, name='red_de_palabras_ig'),
    
    
]
