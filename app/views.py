# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""
import io
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
from .tasks import *
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from random import randint
import logging
logger = logging.getLogger(__name__)


@login_required(login_url="/login/")
def index(request):
    context = {}
    user = request.user
    user_id = user.id
    '''
    if user.groups.filter(name='Administrador').exists():
        try:
            return render(request, "index_admin.html")
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'horizontal-page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'horizontal-page-500.html' )
            return HttpResponse(html_template.render(context, request))
    '''
    
    if user.groups.filter(name='Publicista').exists() or user.groups.filter(name='Administrador').exists():
        # Data for the cards
        datas = []
        colors = ['bg-c-blue', 'bg-c-green', 'bg-c-yellow', 'bg-c-red']
        top_post = (cuentas_empresa.objects
                    .order_by('-post_count')
                    .values_list('post_count', 'username')
                    .distinct()).values()[:4]

        for idx, value in enumerate(top_post):
            campana_id = value['data_red_campana_id']
            post_account = value['post_count']
            campana = campana_publicitaria.objects.filter(id=campana_id).values()
            for campana_value in campana:
                campana_name = campana_value['nombre_campana']

            data = {
                'campana_name': campana_name,
                'post_account':post_account,
                'color': colors[idx]
            }

            datas.append(data)

        #Data for the table
        empresas_to_list = empresa.objects.all()

        #Data for the chart
        esuchas_store = escucha.objects.all()
        list_escuchas = []
        dict_f = {}
        for escucha_store in esuchas_store:
            escucha_data_store = data_red.objects.filter(data_red_escucha__id=escucha_store.id).count()
            list_escuchas.append(escucha_data_store)
            dict_f[escucha_store.nombre_escucha]=escucha_data_store

        values_list=list(dict_f.values())
        new_values = list(dict_f.values())
        key_list = list(dict_f.keys())


        final_list = []
        for i in range(0, 3):
            max1 = 0
            for j in range(len(values_list)):
                if values_list[j] > max1:
                    max1 = values_list[j]
            if values_list:
                values_list.remove(max1)
                final_list.append(max1)
        
        labels=[]
        for item in final_list:
            position = new_values.index(item)
            labels.append(key_list[position])

        
        data = {
            'labels': labels,
            'datasets': [
                {
                    'label': "Escuchas con más datos",
                    'backgroundColor': ["#3e95cd", "#0047CC", "#172A4D", "#002D80", "#001233", "#73b4ff"],
                    'data': final_list
                }
            ]
        }

        #Data social media
        instagram = red_social.objects.filter(nombre_red_social="Instagram").values()
        for value in instagram:
            insta_iden = value['id']
        
        facebook = red_social.objects.filter(nombre_red_social="Facebook").values()
        for value in facebook:
            face_iden = value['id']

        twitter = red_social.objects.filter(nombre_red_social="Twitter").values()
        for value in twitter:
            twitt_iden = value['id']

        data_instagram = data_red.objects.filter(data_red_social=insta_iden).count()
        data_facebook = data_red.objects.filter(data_red_social=face_iden).count()
        data_twitter = data_red.objects.filter(data_red_social=twitt_iden).count()

        try:
            return render(request, "index_publicist.html", 
                {
                    "empresas":empresas_to_list, 
                    'datas': datas, 
                    'pie_chart': data, 
                    'data_instagram':data_instagram,
                    'data_facebook':data_facebook,
                    'data_twitter':data_twitter
                }
            )
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'horizontal-page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'horizontal-page-500.html' )
            return HttpResponse(html_template.render(context, request))

    if user.groups.filter(name='Cliente').exists():
        empresa_id = 0
        dataset_followers_twit = {}

        empresa_user = empresa.objects.filter(usuarios__id=user_id).values()
        if empresa_user:
            for value in empresa_user:
                empresa_id = value['id']
        
        campanas_empresa = campana_publicitaria.objects.filter(empresa_campana__id=empresa_id).values()
        if campanas_empresa:
            for campana_empresa in campanas_empresa:
                cuenta_campana = cuentas_empresa.objects.filter(data_red_campana__id=campana_empresa['id']).values()
                if cuenta_campana:
                    colors = ['#59A8FF', '#51C0E8', '#66FEFF', '#51E8BD', '#59FFA1']
                    usernames = []
                    background_colors = []
                    values = []
                    for cuenta in cuenta_campana:
                        index_color = randint(0,len(colors)-1)
                        background_colors.append(colors[index_color])

                        username = cuenta['username']
                        post_count = cuenta['post_count']
                        
                        usernames.append(username)
                        values.append(post_count)
                        

                    dataset_followers_twit =  {
                        'labels': usernames,
                        'datasets': [
                            {
                                'label': 'Número de publicaciones',
                                'backgroundColor': background_colors,
                                'data': values
                            }
                        ]
                    }


        official_escuchas = escucha.objects.filter(empresa_red_social__id=empresa_id).filter(es_competencia=False).count()
        unofficial_escuchas = escucha.objects.filter(empresa_red_social__id=empresa_id).filter(es_competencia=True).count()

        data = {
            'labels': ['Escuchas de la competencia', 'Escuchas oficiales'],
            'datasets': [
                {
                    'label': "Distribución de las escuchas",
                    'backgroundColor': ["#3e95cd", "#0047CC"],
                    'data': [unofficial_escuchas, official_escuchas]
                }
            ]
        }


        try:
            return render(request, "index_client.html", {
                'empresa_id': empresa_id, 
                'data_followers_twit': dataset_followers_twit,
                'pie_chart': data
            })
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'horizontal-page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'horizontal-page-500.html' )
            return HttpResponse(html_template.render(context, request))

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

@login_required(login_url="/login/")
def acerca_de(request):
    context = {}
    user = request.user
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        try:
            return render(request, "acerca_de.html")
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def empresas(request):        
    context = {}
    user = request.user
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        empresas_to_list = empresa.objects.all()
        try:
            return render(request, "empresas.html",{"empresas":empresas_to_list})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def campanas_publicitarias(request):
    context = {}
    user = request.user
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        campanas_publicitarias_to_list = campana_publicitaria.objects.all()
        try:
            return render(request, "campanas.html",{"campanas_publicitarias":campanas_publicitarias_to_list})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def redes_sociales(request):
    context = {}
    user = request.user
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        redes_sociales_to_list = red_social.objects.all()
        try:
            return render(request, "redes_sociales.html", {"redes_sociales":redes_sociales_to_list})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def ubicaciones(request):    
    context = {}
    user = request.user
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        ubicaciones = ubicacion.objects.all()
        try:
            return render(request, "ubicaciones.html", {"ubicaciones":ubicaciones})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def hashtags(request):    
    context = {}
    user = request.user
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        hashtags = hashtag.objects.all()
        try:
            return render(request, "hashtags.html", {"hashtags":hashtags})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def redes_data(request):        
    user = request.user
    context = {}
    if user.groups.filter(name='Administrador').exists():
        data_redes = data_red.objects.all()
        try:
            return render(request, "redes_data.html", {"redes_data":data_redes})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))
        
@login_required(login_url="/login/")
def cuentas(request):        
    user = request.user
    context = {}
    if user.groups.filter(name='Administrador').exists():
        cuentas = cuentas_empresa.objects.all()
        try:
            return render(request, "cuentas.html", {"cuentas":cuentas})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def escuchas_campana(request, campana_id):
    user = request.user
    context = {}
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        today = date.today()
        escuchas = []
        escuchas = escucha.objects.filter(campana_publicitaria_red_social__id=campana_id).values()

        for escucha_record in escuchas:
            date_start = escucha_record['fecha_inicio_red_social']
            data_finish = escucha_record['fecha_final_red_social']
            
            if data_finish >= today:
                escucha_id = escucha_record['id']

                search_user = escucha_record['usuario_red_social']
                if search_user.startswith('@'):
                    search_user.replace(search_user[0], '')

                escucha_hashtags = hashtag.objects.filter(escucha__id=escucha_record['id']).values()
                hastags_ids_list = []
                for escucha_hashtag in escucha_hashtags:
                    hashtag_id = escucha_hashtag['id']
                    hastags_ids_list.append(hashtag_id)

                escucha_empresas = empresa.objects.filter(escucha__id=escucha_record['id']).values()
                for escucha_empresa in escucha_empresas:
                    escucha_empresa_id = escucha_empresa['id']

                escucha_campana_values = campana_publicitaria.objects.filter(escucha__id=escucha_record['id']).values()
                for escucha_campana_value in escucha_campana_values:
                    campana_id = escucha_campana_value['id']

                escucha_credenciales = escucha_credencial.objects.filter(escucha__id=escucha_record['id']).values()
                for credencial in escucha_credenciales:
                    twitter_bearer_token = credencial['twitter_bearer_token']
                    instagram_user = credencial['instagram_username']
                    instagram_pass = credencial['instagram_password']
                    instagram_path = credencial['instagram_path']

                redes_sociales = red_social.objects.filter(escucha__id=escucha_record['id']).values()

                for red in redes_sociales:
                    id_red = red['id']
                    nombre_red = red['nombre_red_social']
                    
                    if nombre_red == "Facebook":
                        facebook_posts = get_facebook_post(
                            nombre_pagina=search_user, 
                            numero_paginas = 100,
                            id_campana = campana_id,
                            id_escucha = escucha_id,
                            id_red = id_red
                        )
                    
                    if nombre_red == "Twitter":
                        
                        twitter_data = {
                            'nombre_usuario':search_user, 
                            'bearer_token':twitter_bearer_token, 
                            'id_campana':campana_id, 
                            'id_escucha':escucha_id,
                            'id_red':id_red
                        }
                        
                        ## Tasks
                        obtener_account_user(data=twitter_data)
                        obtener_twitters_user(data=twitter_data)
                        

                        for escucha_hashtag in escucha_hashtags:
                            nombre_hashtag = escucha_hashtag['nombre_hastag']
                            hashtag_data = {
                                'query': nombre_hashtag,
                                'bearer_token': twitter_bearer_token, 
                                'id_campana': campana_id, 
                                'id_escucha': escucha_id,
                                'id_red': id_red
                            }
                            obtener_twitters_query(
                                data = hashtag_data
                            )
                    
                    '''
                    if nombre_red == "Instagram":
                        search_accounts = search_accounts_by_username(
                            nombre_pagina=search_user, 
                            #empresa_id=empresa_id, 
                            username=instagram_user, 
                            password=instagram_pass, 
                            path=instagram_path,
                            hashtag_list = hastags_ids_list,
                            id_campana=campana_id, 
                            id_escucha=escucha_id,
                            id_red = id_red
                        )
                    '''

        try:
            return render(request, "escuchas_empresa.html", {"escuchas":escuchas})
        except template.TemplateDoesNotExist:
            html_template = loader.get_template( 'page-404.html' )
            return HttpResponse(html_template.render(context, request))
        except:
            html_template = loader.get_template( 'page-500.html' )
            return HttpResponse(html_template.render(context, request))
    else:
        html_template = loader.get_template( 'page-403.html' )
        return HttpResponse(html_template.render(context, request))

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
                msg     = messages.success(request, 'Empresa guardada.')
                success = True
                return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success })
        return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success }) 
    else:
        if request.method == 'GET':
            if id!=0:
                emp = empresa.objects.get(pk=id)
                form = empresa_form(instance = emp)
                return render(request, 'crear_empresa.html', {'form': form, "msg" : msg, "success" : success })

@login_required(login_url="/login/")
def add_camapana_publicitaria(request, id=0):
    msg     = None
    success = False  
    user = request.user
    form = campana_publicitaria_form()
    ubication_form = ubicacion_form()
    bussines_form = empresa_form()

    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():        
        if request.method == 'GET':
            if id==0:
                form = campana_publicitaria_form()
            else:
                emp = campana_publicitaria.objects.get(pk=id)
                form = campana_publicitaria_form(instance = emp)                
            return render(request, 'crear_campana_publicitaria.html', {'form': form, "msg" : msg, "success" : success, "ubication_form": ubication_form, "empresa_form": bussines_form})
        else:
            if id==0:
                form = campana_publicitaria_form(request.POST)
            else:                 
                emp = campana_publicitaria.objects.get(pk=id)
                form = campana_publicitaria_form(request.POST, instance = emp)

            if ubication_form.is_valid():
                edit_ubication = ubication_form.save()

            if bussines_form.is_valid():
                edit_empresa = bussines_form.save()

            if form.is_valid():
                edit_campana = form.save()
                msg     = 'Campana Publicitaria guardada.'
                success = True
                return render(request, 'crear_campana_publicitaria.html', {'form': form, "msg" : msg, "success" : success , "ubication_form": ubication_form, "empresa_form": bussines_form})
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied
    return render(request, 'crear_campana_publicitaria.html', {'form': form, "msg" : msg, "success" : success, "ubication_form": ubication_form, "empresa_form": bussines_form})

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
    form_credential = credenciales_form()
    hashtags_form = hashtag_form()
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = escucha_form(request.POST) # Bound form
            if form_credential.is_valid():
                edit_credential = form_credential.save()

            if hashtags_form.is_valid():
                edit_hashtag = hashtags_form.save()

            if form.is_valid():
                new_escucha = form.save() # Guardar los datos en la base de datos
                msg     = 'Escucha creada.'
                success = True
                # return HttpResponseRedirect(reverse('redes_sociales'))
        else:
            form = escucha_form() # Unbound form
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied    

    return render(request, 'crear_escuchas.html', {'form': form, "msg" : msg, "success" : success, 'form_credential': form_credential, 'hashtags_form': hashtags_form})

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

@login_required(login_url="/login/")
def add_credential(request):
    msg     = None
    success = False    
    user = request.user   
    form = credenciales_form()
    if user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Publicista').exists():        
        if request.method == 'POST': # si el usuario está enviando el formulario con datos
            form = credenciales_form(request.POST) # Bound form
            if form.is_valid():
                new_credential = form.save() # Guardar los datos en la base de datos
                msg     = 'Credenciales guardadas.'
                success = True
                #return HttpResponseRedirect(reverse('redes_sociales'))
        else:
            form = credenciales_form() # Unbound form
    elif user.groups.filter(name='Cliente').exists():
        raise PermissionDenied

    return render(request, 'crear_credenciales.html', {'form': form, "msg" : msg, "success" : success })  

@login_required(login_url="/login/")
def campanas_empresa(request, empresa_id):
    context = {}
    campanas = []

    if empresa_id !=0:
        empresa_user = empresa.objects.filter(id=empresa_id).values()

        for value in empresa_user:
            empresa_id = value['id']
        campanas = campana_publicitaria.objects.filter(empresa_campana__id=empresa_id).values()

        cuentas = []
        for campana_value in campanas:
            cuentas_campana = cuentas_empresa.objects.filter(data_red_campana__id=campana_value['id']).values()
            for cuentas_value in cuentas_campana:
                account = cuentas_value['username']
                followers = cuentas_value['followers_count']
                account_dict = {
                    'account': account,
                    'followers': followers
                }
                cuentas.append(account_dict)

            data_hashtag = data_red.objects.filter(data_red_campana__id=campana_value['id']).filter(is_from_hashtag=True).count()
            data_account = data_red.objects.filter(data_red_campana__id=campana_value['id']).filter(is_from_hashtag=False).count()

            data = {
                'labels': ['Datos de hashtag', 'Datos de cuentas'],
                'datasets': [
                    {
                        'label': "Distribución de los datos",
                        'backgroundColor': ["#3e95cd", "#0047CC"],
                        'data': [data_hashtag, data_account]
                    }
                ]
            }

    try:
        return render(request, "campanas_empresa.html", {
            'campanas':campanas, 
            'cuentas': cuentas, 
            'data_hashtag':data_hashtag, 
            'data_account':data_account,
            'pie_chart': data
        })
    except template.TemplateDoesNotExist:
        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))    
    
