# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(estado_empresa)
admin.site.register(empresa)
admin.site.register(campana_publicitaria)
admin.site.register(red_social)
admin.site.register(ubicacion)
admin.site.register(hashtag) 
admin.site.register(data_red)
admin.site.register(escucha)
admin.site.register(escucha_credencial)
