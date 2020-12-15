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
        for campana_publicitaria_to_list in campanas_publicitarias_to_list:
            campana_id = campana_publicitaria_to_list.id
            try:
                escucha_campana_values = escucha.objects.filter(campana_publicitaria_red_social__id=campana_id).values()
                continue
            except:
                logger.error("No hay escuchas relacionadas con esta campaña")
            else:
                count_official_escucha = 0
                count_competition_escucha = 0
                for value in escucha_campana_values:
                    escucha_id = value['id']
                    type_escucha = value['es_competencia']
                    if type_escucha == False or type_escucha == 0:
                        count_official_escucha += 1
                        try:
                            account_escucha_campana_values = cuentas_empresa.objects.filter(escucha__id=escucha_id).values()
                            continue
                        except:
                            logger.error("No hay cuentas para esta escucha")
                        else:
                            official_account_count = 0
                            for account_value in account_escucha_campana_values:
                                official_account_count += 1
                                account_id = account_value['id']
                        #data_escucha_campana_values = data_red.objects.filter(campana_publicitaria_red_social__id=campana_id).values()
                
                    else:
                        count_competition_escucha += 1
                        try:
                            account_escucha_campana_values = cuentas_empresa.objects.filter(escucha__id=escucha_id).values()
                            continue
                        except:
                            logger.error("No hay cuentas para esta escucha")
                        else:
                            unofficial_account_count = 0
                            for account_value in account_escucha_campana_values:
                                unofficial_account_count += 1
                                account_id = account_value['id']

                official_info_dict = {
                    'official_escucha_number': count_official_escucha,
                    'official_account_number': official_account_count
                }

                unofficial_info_dict = {
                    'unofficial_escucha_number': count_competition_escucha,
                    'unofficial_account_number': unofficial_account_count
                }
                logger.error(official_info_dict)
                logger.error(unofficial_info_dict)
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
    escuchas_to_list = []
    escuchas_to_list = escucha.objects.all().values()
    for escucha_record in escuchas_to_list:
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
        
        list_redes_sociales_id = []
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
                obtener_twitters_user(
                    nombre_usuario=search_user, 
                    bearer_token=twitter_bearer_token, 
                    id_campana=campana_id, 
                    id_escucha=escucha_id,
                    id_red = id_red
                )
                for escucha_hashtag in escucha_hashtags:
                    nombre_hashtag = escucha_hashtag['nombre_hastag']
                    obtener_twitters_query(
                        query=nombre_hashtag, 
                        bearer_token=twitter_bearer_token, 
                        id_campana=campana_id, 
                        id_escucha=escucha_id,
                        id_red = id_red
                    )

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

@login_required(login_url="/login/")
def cuentas(request):        
    user = request.user
    if user.groups.filter(name='Administrador').exists():       
        cuentas = cuentas_empresa.objects.all()
        return render(request, "cuentas.html", {"cuentas":cuentas})

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
def escuchas_campana(request, campana_id):
    escuchas = []
    escuchas = escucha.objects.filter(campana_publicitaria_red_social__id=campana_id).values()

    for escucha_record in escuchas:
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

    return render(request, "escuchas_empresa.html", {"escuchas":escuchas})

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

#******************************
# Nube de palabras
#******************************
# def nube_de_palabras (text):    
    
#         twitter_red_social = red_social.objects.get(nombre_red_social="Twitter")
#         twitter_data_to_list = data_red.objects.filter(data_red_social = twitter_red_social).values('publicacion_texto')
#         text = str(twitter_data_to_list)
        
#         stopwords = set(STOPWORDS)
#         STOPLIST = set(stopwords.words('spanish'))        
#         stopwords.add('RT')
#         stopwords.add('publicacion_texto')
#         stopwords.add("publicacion_texto'")
#         stopwords.add('publicacion_texto RT')
#         stopwords.add('una')
        
#         wordcloud = WordCloud(background_color='white', stopwords=Tok).generate(text)
#         plt.imshow(wordcloud)
#         plt.axis("off")
#         #plt.show()
#         image = io.BytesIO()
#         plt.savefig(image, format='png')
#         image.seek(0)  # rewind the data
#         string = base64.b64encode(image.read())

#         image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
#         return image_64            
#         # 
#         # plt.imshow(wordcloud)
#         # plt.axis("off")
#         # s = plt.show()

# def cloud_gen(request):
#     twitter_red_social = red_social.objects.get(nombre_red_social="Twitter")
#     twitter_data_to_list = data_red.objects.filter(data_red_social = twitter_red_social).values('publicacion_texto')
#     texto = str(twitter_data_to_list)
#     text = ''
    
#     for i in texto:
#         if __name__ == '__main__':
#             text += i.text

#     wordcloud = nube_de_palabras(text)
#     return render(request, "nube_de_palabras.html",{'wordcloud':wordcloud})
