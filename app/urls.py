# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

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
<<<<<<< HEAD
    path('facebook/', views.facebook_data, name='facebook'),
    path('twitter/', views.twitter_data, name='twitter'),
    path('redes/create/', views.add_red_social, name='crear_red'),
=======
    path('redes/save/', views.add_red_social, name='crear_red'),
>>>>>>> upstream/master
    path('ubicacion/', views.add_ubicacion,  name='crear_ubicacion'),
    path('hashtag/', views.add_hashtag, name='crear_hashtag'),
    path('acercade/', views.acerca_de, name='acerca_de'),
    re_path(r'^empresas/save/(?P<id>\w+)/$', views.add_empresas, name='editar_empresa'),
    re_path(r'^empresas/delete/(?P<id>\w+)/$', views.delete_empresas, name='eliminar_empresa'),
    re_path(r'^redes/save/(?P<id>\w+)/$', views.add_red_social, name='editar_redes'),
    re_path(r'^redes/delete/(?P<id>\w+)/$', views.delete_red_social, name='eliminar_redes'),
    re_path(r'^campanas/save/(?P<id>\w+)/$', views.add_camapana_publicitaria, name='editar_campana'),
    re_path(r'^campanas/delete/(?P<id>\w+)/$', views.delete_camapana_publicitaria, name='eliminar_campana'),
]
