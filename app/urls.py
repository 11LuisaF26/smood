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
    path('empresas/create/', views.add_empresas, name='crear_empresa'),
    path('campanas/', views.campanas_publicitarias, name='campanas_publicitarias'),
    path('campanas/create/', views.add_camapana_publicitaria, name='crear_campana'),
    path('redes/',  views.redes_sociales, name='redes_sociales'),
    path('redes/create/', views.add_red_social, name='crear_red'),
    path('ubicacion/', views.add_ubicacion,  name='crear_ubicacion'),
    path('hashtag/', views.add_hashtag, name='crear_hashtag'),
    path('acercade/', views.acerca_de, name='acerca_de'),
]
