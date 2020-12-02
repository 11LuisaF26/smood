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
def get_facebook_post(nombre_pagina, numero_paginas, id_campana, id_escucha, id_red):
    data_escucha = escucha.objects.get(id=id_escucha)
    data_campana = campana_publicitaria.objects.get(id=id_campana)
    data_red_social = red_social.objects.get(id=id_red)
    for publicacion in get_posts(nombre_pagina, pages=numero_paginas):
        if publicacion and publicacion["post_id"]:
            data_red_escucha = data_red.objects.filter(publicacion_id=publicacion["post_id"],data_red_escucha=data_escucha, data_red_campana=data_campana).values()
            if not data_red_escucha:
                new_publication = data_red(
                    publicacion_id = publicacion["post_id"], 
                    publicacion_fecha = publicacion["post_text"][:200],
                    publicacion_texto = publicacion["time"], 
                    publicacion_likes = publicacion["likes"],
                    publicacion_comentarios = publicacion["comments"],
                    publicacion_compartidos = publicacion["shares"],
                    publicacion_user = publicacion["user_id"],
                    data_red_escucha = data_escucha,
                    data_red_campana = data_campana,
                    data_red_social = data_red_social
                )
                new_publication.save()
    logger.error('Task get facebook post completed succesfully')
    
@background(schedule=5)
def obtener_twitters_user(nombre_usuario, bearer_token, id_campana, id_escucha, id_red):
    data_escucha = escucha.objects.get(id=id_escucha)
    data_campana = campana_publicitaria.objects.get(id=id_campana)
    data_red_social = red_social.objects.get(id=id_red)
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
            if data and data["id"]:
                data_red_escucha = data_red.objects.filter(publicacion_id=data["id"],data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                if not data_red_escucha:
                    new_publication = data_red(
                        publicacion_id = data["id"],
                        publicacion_texto = data["text"][:200],
                        publicacion_fecha = data["created_at"],
                        publicacion_likes = data["public_metrics"]["like_count"],
                        publicacion_comentarios = data["public_metrics"]["reply_count"],
                        publicacion_compartidos = data["public_metrics"]["retweet_count"],
                        publicacion_user = data["author_id"],
                        data_red_escucha = data_escucha,
                        data_red_campana = data_campana,
                        data_red_social = data_red_social
                    )
                    new_publication.save()
                
@background(schedule=5)
def obtener_twitters_query(query, bearer_token, id_campana, id_escucha, id_red):
    data_escucha = escucha.objects.get(id=id_escucha)
    data_campana = campana_publicitaria.objects.get(id=id_campana)
    data_red_social = red_social.objects.get(id=id_red)
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
            if data and data["id"]:
                data_red_escucha = data_red.objects.filter(publicacion_id=data["id"],data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                if not data_red_escucha:
                    new_publication = data_red(
                        publicacion_id = data["id"], 
                        publicacion_fecha = data["text"][:200],
                        publicacion_texto = data["created_at"], 
                        publicacion_likes = data["public_metrics"]["like_count"],
                        publicacion_comentarios = data["public_metrics"]["retweet_count"],
                        publicacion_compartidos = data["public_metrics"]["retweet_count"],
                        publicacion_user = data["author_id"],
                        is_from_hashtag = True,
                        data_red_escucha = data_escucha,
                        data_red_campana = data_campana,
                        data_red_social = data_red_social
                    )
                    new_publication.save()

@background(schedule=5)
def search_accounts_by_username(nombre_pagina, username, password, path, hashtag_list, id_campana, id_escucha, id_red):
    data_escucha = escucha.objects.get(id=id_escucha)
    data_campana = campana_publicitaria.objects.get(id=id_campana)
    data_red_social = red_social.objects.get(id=id_red)
    instagram = Instagram()
    instagram.with_credentials(username, password, path)
    try:
        instagram.login(True)
    except:
        logger.error("*********************************************************************************")
        logger.error("No hemos podido ingresar a instagram en la tarea de obtener cuentas por tag")
        logger.error("********************************************************************************")
    else:
        try:
            accounts = instagram.search_accounts_by_username(nombre_pagina)
        except:
            logger.error("*********************************************************************************")
            logger.error("No se han encontrado datos de cuentas en la tarea de obtener cuentas por tag")
            logger.error("********************************************************************************")
        else:
            for account in accounts:
                if account.is_verified == True and account.username:
                    data_red_cuentas = cuentas_empresa.objects.filter(username=account.username,data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                    if not data_red_cuentas:
                        new_account = cuentas_empresa(
                            identifier = account.identifier, 
                            username = account.username,
                            fullname = account.full_name, 
                            profile_pic_url = account.profile_pic_url,
                            data_red_escucha = data_escucha,
                            data_red_campana = data_campana,
                            data_red_social = data_red_social
                        )
                        new_account.save()
            logger.error('Task get instagram accounts has finished succesfully')
    
    '''
    get_instagram_medias_by_user(username=username, password=password, path=path, id_campana=id_campana, id_escucha= id_escucha, id_red=id_red)
    '''
    get_instagram_medias_by_tag(username=username, password=password, path=path, list_hashtag_ids=hashtag_list, id_campana=id_campana, id_escucha= id_escucha, id_red=id_red)
    
'''
@background(schedule=5)
def get_instagram_medias_by_user(username, password, path, id_campana, id_escucha, id_red):
    data_escucha = escucha.objects.get(id=id_escucha)
    data_campana = campana_publicitaria.objects.get(id=id_campana)
    data_red_social = red_social.objects.get(id=id_red)
    instagram = Instagram()
    instagram.with_credentials(username, password, path)

    cuentas_empresas = cuentas_empresa.objects.filter(data_red_escucha=data_escucha, data_red_campana=data_campana).values()
    try:
        instagram.login(True)
    except:
        logger.error("*********************************************************************************")
        logger.error("No se ha podido ingresar a instagram en la tarea de obtener medias por username")
        logger.error("*********************************************************************************")
    else:
        for cuenta in cuentas_empresas:
            username_search = cuenta['username']
            medias = instagram.get_medias(username_search, 100)
            for media in medias:
                if media.identifier:
                    new_publication = data_red(
                        publicacion_id = media.identifier, 
                        publicacion_fecha = media.created_time,
                        publicacion_texto = media.caption, 
                        publicacion_likes = media.likes_count,
                        publicacion_comentarios = media.comments_count,
                        publicacion_compartidos = 0,
                        publicacion_user = media.owner.identifier,
                        data_red_escucha = data_escucha,
                        data_red_campana = data_campana,
                        data_red_social = data_red_social
                    )
                    new_publication.save()
        logger.error('Task get instagram medias by username has finished succesfully')
'''


@background(schedule=5)
def get_instagram_medias_by_tag(username, password, path, list_hashtag_ids, id_campana, id_escucha, id_red): 
    data_escucha = escucha.objects.get(id=id_escucha)
    data_campana = campana_publicitaria.objects.get(id=id_campana)
    data_red_social = red_social.objects.get(id=id_red)

    instagram = Instagram()
    instagram.with_credentials(username, password, path)
    
    try:
        instagram.login(True)
    except:
        logger.error("********************************************************************************")
        logger.error("No hemos podido ingresar a instagram en la tarea de obtener medias por tag")
        logger.error("*******************************************************************************")
    else:
        for hashtag_id in list_hashtag_ids:
            escucha_hashtag = hashtag.objects.filter(id=hashtag_id).values()
            
            for value in escucha_hashtag:
                nombre_hashtag = value['nombre_hastag']
                if nombre_hashtag.startswith('#'):
                    nombre_hashtag = nombre_hashtag.replace(nombre_hashtag[0], '')
            
                medias = instagram.get_medias_by_tag(nombre_hashtag, count=100)
                
                for media in medias:
                    if media.identifier:
                        data_red_tag = data_red.objects.filter(publicacion_id=media.identifier,data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                        if not data_red_tag:
                            new_publication = data_red(
                                publicacion_id = media.identifier, 
                                publicacion_fecha = media.created_time,
                                publicacion_texto = media.caption, 
                                publicacion_likes = media.likes_count,
                                publicacion_comentarios = media.comments_count,
                                publicacion_compartidos = 0,
                                publicacion_user = media.owner.identifier,
                                is_from_hashtag = True,
                                data_red_escucha = data_escucha,
                                data_red_campana = data_campana,
                                data_red_social = data_red_social
                            )
                            new_publication.save()

        logger.error('Task get instagram medias by tag has finished succesfully')
