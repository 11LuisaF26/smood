# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect 
from django import template
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.template import RequestContext
from django.views.generic import CreateView, ListView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *
from app import tasks
import logging
logger = logging.getLogger(__name__)

@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template = request.path.split('/')[-1]
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))
    
    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

#******************************
# Acerca de
#******************************
@login_required(login_url="/login/")
def acerca_de(request):
    return render(request, "acerca_de.html")


#******************************
# Funciones para listar
#******************************

@login_required(login_url="/login/")
def empresas(request):        
    user = request.user
    if user.groups.filter(name='Administrador').exists():       
        empresas_to_list = empresa.objects.all()
    else:   
        empresas_to_list = empresa.objects.filter(usuarios = request.user)
    return render(request, "empresas.html", {"empresas":empresas_to_list})

@login_required(login_url="/login/")
def campanas_publicitarias(request):
    user = request.user
    if user.groups.filter(name='Administrador').exists():       
        campanas_publicitarias_to_list = campana_publicitaria.objects.all()
    else:
        empresas = empresa.objects.filter(usuarios = request.user)
        campanas_publicitarias_to_list = campana_publicitaria.objects.filter(empresa_campana__in = empresas)
    return render(request, "campanas.html", {"campanas_publicitarias":campanas_publicitarias_to_list})

@login_required(login_url="/login/")
def redes_sociales(request):
    redes_sociales_to_list = red_social.objects.all()
    return render(request, "redes_sociales.html", {"redes_sociales":redes_sociales_to_list})

@login_required(login_url="/login/")
def escuchas(request):
    escuchas_to_list = escucha.objects.all()
    return render(request, "escuchas.html", {"escuchas":escuchas_to_list})

@login_required(login_url="/login/")
def ubicaciones(request):    
    ubicaciones = ubicacion.objects.all()
    return render(request, "ubicaciones.html", {"ubicaciones":ubicaciones})

@login_required(login_url="/login/")
def hashtags(request):    
    hashtags = hashtag.objects.all()
    return render(request, "hashtags.html", {"hashtags":hashtags})

@login_required(login_url="/login/")
def redes_data(request):        
    user = request.user
    if user.groups.filter(name='Administrador').exists():       
        data_redes = data_red.objects.all()
        return render(request, "redes_data.html", {"redes_data":data_redes})

#******************************
# Funciones para insertar
#******************************
@login_required(login_url="/login/")
def add_empresas(request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = empresa_form()    
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():        
        if request.method == 'GET':
            if id==0:
                form = empresa_form()
            else:
                emp = empresa.objects.get(pk=id)
                form = empresa_form(instance = emp)                
            return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success })
        else:
            if id==0:
                form = empresa_form(request.POST)
            else:                 
                emp = empresa.objects.get(pk=id)
                form = empresa_form(request.POST, instance = emp)
            if form.is_valid():
                edit_empresa = form.save()
                msg     = 'Empresa guardada.'
                success = True
                return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success })
        return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success }) 

@login_required(login_url="/login/")
def add_camapana_publicitaria(request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = campana_publicitaria_form()   
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():        
        if request.method == 'GET':
            if id==0:
                form = campana_publicitaria_form()
            else:
                emp = campana_publicitaria.objects.get(pk=id)
                form = campana_publicitaria_form(instance = emp)                
            return render(request, 'crear_campana_publicitaria.html', {'form': form, "msg" : msg, "success" : success })
        else:
            if id==0:
                form = campana_publicitaria_form(request.POST)
            else:                 
                emp = campana_publicitaria.objects.get(pk=id)
                form = campana_publicitaria_form(request.POST, instance = emp)

            if form.is_valid():
                edit_campana = form.save()
                msg     = 'Campana Publicitaria guardada.'
                success = True
                return render(request, 'crear_campana_publicitaria.html', {'form': form, "msg" : msg, "success" : success })
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied
    return render(request, 'crear_campana_publicitaria.html', {'form': form, "msg" : msg, "success" : success })

@login_required(login_url="/login/")
def add_red_social(request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = red_social_form()
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = red_social_form(request.POST) # Bound form
            if form.is_valid():
                new_red_social = form.save() # Guardar los datos en la base de datos
                msg     = 'Red social creada.'
                success = True
                # return HttpResponseRedirect(reverse('redes_sociales'))
        else:
            form = red_social_form() # Unbound form
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied    

    return render(request, 'crear_redes_sociales.html', {'form': form, "msg" : msg, "success" : success })

@login_required(login_url="/login/")
def add_ubicacion(request):
    msg     = None
    success = False  
    user = request.user
    form = ubicacion_form()
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():        
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = ubicacion_form(request.POST) # Bound form
            if form.is_valid():
                new_ubicacion = form.save() # Guardar los datos en la base de datos
                msg     = 'Ubicacion creada.'
                success = True
                #return HttpResponseRedirect(reverse('redes_sociales'))
        else:
            form = ubicacion_form() # Unbound form
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied


    return render(request, 'crear_ubicacion.html', {'form': form, "msg" : msg, "success" : success })

@login_required(login_url="/login/")
def add_hashtag(request):
    msg     = None
    success = False    
    user = request.user   
    form = hashtag_form()
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():        
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = hashtag_form(request.POST) # Bound form
            if form.is_valid():
                new_hashtag = form.save() # Guardar los datos en la base de datos
                msg     = 'Hashtag creado.'
                success = True
                #return HttpResponseRedirect(reverse('redes_sociales'))
        else:
            form = hashtag_form() # Unbound form
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied

    return render(request, 'crear_hashtag.html', {'form': form, "msg" : msg, "success" : success })  

@login_required(login_url="/login/")
def add_escuchas(request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = escucha_form() 
    logger.error(request.method)
    logger.error(user.groups)
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        logger.error(request.method)
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            logger.error("if method post")
            form = escucha_form(request.POST) # Bound form
            if form.is_valid():
                new_escucha = form.save() # Guardar los datos en la base de datos
                msg     = 'Escucha creada.'
                success = True
                # return HttpResponseRedirect(reverse('redes_sociales'))
        else:
            form = escucha_form() # Unbound form
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied    

    return render(request, 'crear_escuchas.html', {'form': form, "msg" : msg, "success" : success })

@login_required(login_url="/login/")
def delete_empresas (request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = empresa_form()    
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists(): 
        emp = empresa.objects.get(pk=id)
        emp.delete()
        msg     = 'Empresa eliminada.'
        success = True
        return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success })
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied
    return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success })

@login_required(login_url="/login/")
def delete_red_social (request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = red_social_form()  
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists(): 
        red = red_social.objects.get(pk=id)
        red.delete()
        msg     = 'Red social eliminada.'
        success = True
        return render(request, 'crear_redes_sociales.html', {'form': form, "msg" : msg, "success" : success })
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied
    return render(request, 'crear_redes_sociales.html', {'form': form, "msg" : msg, "success" : success })
    
@login_required(login_url="/login/")
def delete_escucha (request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = escucha_form()  
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists(): 
        escucha_d = escucha.objects.get(pk=id)
        escucha_d.delete()
        msg     = 'Escucha eliminada.'
        success = True
        return render(request, 'crear_escuchas.html', {'form': form, "msg" : msg, "success" : success })
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied
    return render(request, 'crear_escuchas.html', {'form': form, "msg" : msg, "success" : success })

@login_required(login_url="/login/")
def delete_camapana_publicitaria (request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = campana_publicitaria_form()  
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists(): 
        camp = campana_publicitaria.objects.get(pk=id)
        camp.delete()
        msg     = 'Campaña eliminada.'
        success = True
        return render(request, 'campanas.html', {'form': form, "msg" : msg, "success" : success })
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied
    return render(request, 'campanas.html', {'form': form, "msg" : msg, "success" : success })