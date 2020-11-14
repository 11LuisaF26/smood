# -*- coding: utf-8 -*-
from background_task import background
from django.contrib.auth.models import User
from facebook_scraper import get_posts
from igramscraper.instagram import Instagram
from app.models import *
from requests.exceptions import HTTPError, ConnectionError, Timeout
from . import twitter_conn
import logging
import json
logger = logging.getLogger(__name__)

@background(schedule=5)
def get_facebook_post(nombre_pagina, numero_paginas, id_red_social):
    data_redes = data_red.objects.all().values()
    list_publication_ids = []
    for data in data_redes:
        list_publication_ids.append(data["publicacion_id"])
    
    for publicacion in get_posts(nombre_pagina, pages=numero_paginas):    
        if publicacion and publicacion["post_id"] not in list_publication_ids:
            publicacion_id = publicacion["post_id"]
            publicacion_texto = publicacion["post_text"][:200]
            publicacion_fecha = publicacion["time"]
            publicacion_likes = publicacion["likes"]
            publicacion_comentarios = publicacion["comments"]
            publicacion_compartidos = publicacion["shares"]
            publicacion_user = publicacion["user_id"]
            red_social_interes = red_social.objects.get(id=id_red_social)
            
            new_publication = data_red(
                publicacion_id = publicacion_id, 
                publicacion_fecha = publicacion_fecha,
                publicacion_texto = publicacion_texto, 
                publicacion_likes = publicacion_likes,
                publicacion_comentarios = publicacion_comentarios,
                publicacion_compartidos = publicacion_compartidos,
                publicacion_user = publicacion_user,
                data_red_social = red_social_interes
            )
            new_publication.save()
    
@background(schedule=5)
def obtener_twitters_user(nombre_usuario, bearer_token, id_red_social):
    data_redes = data_red.objects.all().values()
    list_publication_ids = []
    for data in data_redes:
        list_publication_ids.append(data["publicacion_id"])

    conn = twitter_conn.TwitterConn(access_token=bearer_token)
    
    try:
        response_user_tweets = conn.obtener_twiiter_user(nombre_usuario=nombre_usuario)
        response_user_tweets.raise_for_status()
    except (ConnectionError, TimeoutError) as e:
        logger.error(str(e))
        raise ValidationError("ConnectionError or TimeoutError")
    except HTTPError as e:
        logger.error(str(e))
        raise ValidationError("HTTP Error")
    except Exception as e:
        logger.error(str(e))
        raise ValidationError("Exception")
    else:
        content_response_user_tweets = response_user_tweets.content.decode("utf-8")
        data_response_user_tweets = json.loads(content_response_user_tweets)
        list_data = data_response_user_tweets["data"]

        for data in list_data:
            if data and data["id"] not in list_publication_ids:
                publicacion_id = data["id"]
                publicacion_texto = data["text"][:200]
                publicacion_fecha = data["created_at"]
                publicacion_likes = data["public_metrics"]["like_count"]
                publicacion_comentarios = data["public_metrics"]["reply_count"]
                publicacion_compartidos = data["public_metrics"]["retweet_count"]
                publicacion_user = data["author_id"]
                red_social_interes = red_social.objects.get(id=id_red_social)
                publicacion_id = publicacion_id, 
                publicacion_fecha = publicacion_fecha,
                publicacion_texto = publicacion_texto,
                
                new_publication = data_red(
                            publicacion_likes = publicacion_likes,
                            publicacion_comentarios = publicacion_comentarios,
                            publicacion_compartidos = publicacion_compartidos,
                            publicacion_user = publicacion_user,
                            data_red_social = red_social_interes
                    )
                new_publication.save()
                
@background(schedule=5)
def obtener_twitters_query(query, bearer_token, id_red_social):
    data_redes = data_red.objects.all().values()
    list_publication_ids = []
    for data in data_redes:
        list_publication_ids.append(data["publicacion_id"])

    conn = twitter_conn.TwitterConn(access_token=bearer_token)
    
    try:
        response_query_tweets = conn.obtener_twiiter_query(query=query)
        response_query_tweets.raise_for_status()
    except (ConnectionError, TimeoutError) as e:
        logger.error(str(e))
        raise ValidationError("ConnectionError or TimeoutError")
    except HTTPError as e:
        logger.error(str(e))
        raise ValidationError("HTTP Error")
    except Exception as e:
        logger.error(str(e))
        raise ValidationError("Exception")
    else:
        content_response_query_tweets = response_query_tweets.content.decode("utf-8")
        data_response_query_tweets = json.loads(content_response_query_tweets)
        list_data = data_response_query_tweets["data"]

        for data in list_data:
            if data and data["id"] not in list_publication_ids:
                publicacion_id = data["id"]
                publicacion_texto = data["text"][:200]
                publicacion_fecha = data["created_at"]
                publicacion_likes = data["public_metrics"]["like_count"]
                publicacion_comentarios = data["public_metrics"]["reply_count"]
                publicacion_compartidos = data["public_metrics"]["retweet_count"]
                publicacion_user = data["author_id"]
                red_social_interes = red_social.objects.get(id=id_red_social)

                new_publication = data_red(
                    publicacion_id = publicacion_id, 
                    publicacion_fecha = publicacion_fecha,
                    publicacion_texto = publicacion_texto, 
                    publicacion_likes = publicacion_likes,
                    publicacion_comentarios = publicacion_comentarios,
                    publicacion_compartidos = publicacion_compartidos,
                    publicacion_user = publicacion_user,
                    data_red_social = red_social_interes
                )
                new_publication.save()

@background(schedule=5)
def search_accounts_by_username(nombre_pagina, empresa_id, username, password, path):
    instagram = Instagram()
    instagram.with_credentials(username, password, path)
    try:
        instagram.login(True)
        accounts = instagram.search_accounts_by_username(nombre_pagina)
    except:
        logger.error("******************************")
        logger.error("No pudimos completar la tarea")
        logger.error("******************************")
    else:
        for account in accounts:
            account_identifier = account.identifier
            account_username = account.username
            account_full_name = account.full_name
            account_profile_pic_url = account.profile_pic_url
            account_is_verified = account.is_verified            
            data_cuentas = cuentas_empresa.objects.all().values()
            list_cuentas_username = []
            for data in data_cuentas:
                list_cuentas_username.append(data['username'])
            
            if account_is_verified == True and account_username not in list_cuentas_username:
                empresa_add = empresa.objects.get(id=empresa_id)
                new_account = cuentas_empresa(
                    identifier = account_identifier, 
                    username = account_username,
                    fullname = account_full_name, 
                    profile_pic_url = account_profile_pic_url,
                    empresa = empresa_add
                )
                new_account.save()