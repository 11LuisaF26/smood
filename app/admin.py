# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import csv, datetime

# Register your models here.
admin.site.register(estado_empresa)
admin.site.register(empresa)
admin.site.register(campana_publicitaria)
admin.site.register(red_social)
admin.site.register(ubicacion)
admin.site.register(hashtag) 
# admin.site.register(data_red)
admin.site.register(twitter_credencial) 

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' 'filename{}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)

    return response

export_to_csv.short_description = 'Export to CSV'  #short description

@admin.register(data_red)
class UserAdmin(admin.ModelAdmin):
    actions = [export_to_csv]