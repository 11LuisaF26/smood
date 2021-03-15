# -*- coding: utf-8 -*-
from background_task import background
from django.contrib.auth.models import User
from facebook_scraper import get_posts
# from igramscraper.instagram import Instagram
from app.models import *
from requests.exceptions import HTTPError, ConnectionError, Timeout
from . import twitter_conn
from datetime import datetime
import logging
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
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
                if not publicacion["post_text"] or publicacion["post_text"]==None:
                    publicacion_texto = ""
                else:
                    publicacion_texto = publicacion["post_text"]
                
                new_publication = data_red(
                    publicacion_id = publicacion["post_id"], 
                    publicacion_fecha = publicacion["time"],
                    publicacion_texto = publicacion_texto, 
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
    
@background(schedule=60)
def obtener_account_user(data):
    data_escucha = escucha.objects.get(id=data['id_escucha'])
    data_campana = campana_publicitaria.objects.get(id=data['id_campana'])
    data_red_social = red_social.objects.get(id=data['id_red'])
    escucha_type = data['escucha_type']
    conn = twitter_conn.TwitterConn(access_token=data['bearer_token'])
    try:
        response_account_user = conn.obtener_cuenta_user(nombre_usuario=data['nombre_usuario'])
        response_account_user.raise_for_status()
    except (ConnectionError, TimeoutError) as e:
        logger.error(str(e))
    except HTTPError as e:
        logger.error(str(e))        
    except Exception as e:
        logger.error(str(e))
    else:
        list_data = []
        content_response_user_account = response_account_user.content.decode("utf-8")
        data_response_user_account = json.loads(content_response_user_account)
        if data_response_user_account["data"]:
            list_data = data_response_user_account["data"]

        for data in list_data:
            if data and data["id"]:
                data_cuentas_empresa = cuentas_empresa.objects.filter(identifier=data["id"],data_red_escucha=data_escucha, data_red_campana=data_campana)
                if data_cuentas_empresa:
                    data_cuentas_empresa.followers_count = data["public_metrics"]["followers_count"]
                    data_cuentas_empresa.following_count = data["public_metrics"]["following_count"]
                    data_cuentas_empresa.tweet_count = data["public_metrics"]["tweet_count"]

                if not data_cuentas_empresa:
                    location = ""
                    try:
                        location = data["location"]
                    except:
                        location = ""

                
                    try:
                        etities = data['entities']['url']
                        for entity in etities['urls']:
                            display_url = entity['display_url']
                    except:
                        display_url=""
                    
                    try:
                        display_url = data['url']
                    except:
                        display_url = ""

                    new_cuenta = cuentas_empresa(
                        identifier = data["id"],
                        username = data["username"],
                        fullname = data["name"],
                        profile_pic_url = data["profile_image_url"],
                        created_at = data["created_at"],
                        location = location,
                        followers_count = data["public_metrics"]["followers_count"],
                        following_count = data["public_metrics"]["following_count"],
                        post_count = data["public_metrics"]["tweet_count"],
                        listed_count = data["public_metrics"]["tweet_count"],
                        web_site = display_url,
                        is_competition = escucha_type, 
                        data_red_escucha = data_escucha,
                        data_red_campana = data_campana,
                        data_red_social = data_red_social
                    )
                    new_cuenta.save()

@background(schedule=5)
def obtener_twitters_user(data):
    data_escucha = escucha.objects.get(id=data['id_escucha'])
    data_campana = campana_publicitaria.objects.get(id=data['id_campana'])
    data_red_social = red_social.objects.get(id=data['id_red'])
    conn = twitter_conn.TwitterConn(access_token=data['bearer_token'])
    try:
        response_user_tweets = conn.obtener_twiiter_user(nombre_usuario=data['nombre_usuario'])
        response_user_tweets.raise_for_status()
    except (ConnectionError, TimeoutError) as e:
        logger.error(str(e))
    except HTTPError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
    else:
        list_data = []
        content_response_user_tweets = response_user_tweets.content.decode("utf-8")
        data_response_user_tweets = json.loads(content_response_user_tweets)
        if data_response_user_tweets["data"]:
            list_data = data_response_user_tweets["data"]

        for data in list_data:
            if data and data["id"]:
                data_red_escucha = data_red.objects.filter(publicacion_id=data["id"],data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                if not data_red_escucha:
                    new_publication = data_red(
                        publicacion_id = data["id"],
                        publicacion_texto = data["text"],
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
def obtener_twitters_query(data):
    data_escucha = escucha.objects.get(id=data['id_escucha'])
    data_campana = campana_publicitaria.objects.get(id=data['id_campana'])
    data_red_social = red_social.objects.get(id=data['id_red'])
    conn = twitter_conn.TwitterConn(access_token=data['bearer_token'])
    try:
        response_query_tweets = conn.obtener_twiiter_query(query=data['query'])
        response_query_tweets.raise_for_status()
    except (ConnectionError, TimeoutError) as e:
        logger.error(str(e))
    except HTTPError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(str(e))
    else:
        content_response_query_tweets = response_query_tweets.content.decode("utf-8")
        data_response_query_tweets = json.loads(content_response_query_tweets)

        try:
            list_data = data_response_query_tweets["data"]
        except:
            list_data = []
        else:
            for data in list_data:
                if data and data["id"]:
                    data_red_escucha = data_red.objects.filter(publicacion_id=data["id"],data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                    if not data_red_escucha:
                        new_publication = data_red(
                            publicacion_id = data["id"], 
                            publicacion_fecha = data["created_at"],
                            publicacion_texto = data["text"], 
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
def search_account_by_username(data):
    data_escucha = escucha.objects.get(id=data['id_escucha'])
    data_campana = campana_publicitaria.objects.get(id=data['id_campana'])
    data_red_social = red_social.objects.get(id=data['id_red'])
    escucha_type = data['escucha_type']
    instagram = Instagram()

    try:
        account = instagram.get_account(data['nombre_usuario'])
    except:
        logger.error("*********************************************************************************")
        logger.error("No se ha encontrado datos de cuenta en la tarea de obtener cuenta por tag")
        logger.error("********************************************************************************")
    else:
        data_red_cuentas = cuentas_empresa.objects.filter(username=account.username,data_red_escucha=data_escucha, data_red_campana=data_campana).values()
        if not data_red_cuentas:
            new_account = cuentas_empresa(
                identifier = account.identifier, 
                username = account.username,
                followers_count = account.followed_by_count,
                following_count = account.follows_count,
                post_count = account.media_count,
                listed_count = account.media_count,
                fullname = account.full_name, 
                profile_pic_url = account.profile_pic_url,
                is_competition = escucha_type,
                data_red_escucha = data_escucha,
                data_red_campana = data_campana,    
                data_red_social = data_red_social
            )
            new_account.save()
        logger.error('Task get instagram accounts has finished succesfully')

@background(schedule=5)
def get_instagram_medias_by_user(data):
    data_escucha = escucha.objects.get(id=data['id_escucha'])
    data_campana = campana_publicitaria.objects.get(id=data['id_campana'])
    data_red_social = red_social.objects.get(id=data['id_red'])
    instagram = Instagram()

    try:
        medias = instagram.get_medias(data['nombre_usuario'], 100)
    except:
        logger.error("*********************************************************************************")
        logger.error("Error obteniendo medias por usuario de instagram")
        logger.error("********************************************************************************")
    else:
        for media in medias:
            if media and media.identifier:
                data_red_escucha = data_red.objects.filter(publicacion_id=media.identifier,data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                if not data_red_escucha:

                    try:
                        texto = media.caption
                    except:
                        texto = ""

                    new_publication = data_red(
                        publicacion_id = media.identifier, 
                        publicacion_fecha = datetime.fromtimestamp(media.created_time),
                        publicacion_texto = texto, 
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

@background(schedule=5)
def get_instagram_medias_by_tag(data): 
    data_escucha = escucha.objects.get(id=data['id_escucha'])
    data_campana = campana_publicitaria.objects.get(id=data['id_campana'])
    data_red_social = red_social.objects.get(id=data['id_red'])

    instagram = Instagram()
    
    nombre_hashtag = data['query']
    if nombre_hashtag.startswith('#'):
        nombre_hashtag = nombre_hashtag.replace(nombre_hashtag[0], '')

    try:
        medias = instagram.get_medias_by_tag(nombre_hashtag, count=100)
    except:
        logger.error("*********************************************************************************")
        logger.error("Error obteniendo medias por query de instagram")
        logger.error("********************************************************************************")
    else:
        for media in medias:
            if media.identifier:
                data_red_tag = data_red.objects.filter(publicacion_id=media.identifier,data_red_escucha=data_escucha, data_red_campana=data_campana).values()
                if not data_red_tag:
                    try:
                        texto = media.caption
                    except:
                        texto = ""

                    new_publication = data_red(
                        publicacion_id = media.identifier, 
                        publicacion_fecha = datetime.fromtimestamp(media.created_time),
                        publicacion_texto = texto, 
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

@background(schedule=2)
def analyze_text(account):
    analyze_list = []
    account_datas = data_red.objects.filter(publicacion_user=account['identifier']).values()
    if account_datas:
        for account_data in account_datas:
            if account_data['publicacion_texto']:
                language = _get_language(text=account_data['publicacion_texto'])
                if language and language=="spanish":
                    #analyze = _analyze_spanish_text(text=account_data['publicacion_texto'])
                    #analyze_list.append(analyze)
                    pass
                elif language and language=="english":
                    analyze = _analyze_english_text(text=account_data['publicacion_texto'])
                    analyze_list.append(analyze)
                else:
                    continue
            
            analysis = _get_analysis(analyze_list=analyze_list)
    
    account_object = cuentas_empresa.objects.get(identifier=account['identifier'])
    account_object.avg_compound = analysis
    account_object.save()
            
def _get_language(text):
    languages = ['spanish', 'english']
    tokens = nltk.tokenize.word_tokenize(text)
    tokens = [t.strip().lower() for t in tokens]
    lang_count = {}
    for lang in languages:
        stop_words = nltk.corpus.stopwords.words(lang)
        lang_count[lang] = 0
        for word in tokens:
            if word in stop_words:
                lang_count[lang] += 1
                
    detected_language = max(lang_count, key=lang_count.get)

    return detected_language

def _analyze_spanish_text(text):
    pass

def _analyze_english_text(text):
    sid = SentimentIntensityAnalyzer()
    polarity = sid.polarity_scores(text)
    return polarity

def _get_analysis(analyze_list):
    compound = list([analyze['compound'] for analyze in analyze_list])
    if len(compound) !=0:
        return sum(compound) / len(compound)
    else:
        return 0