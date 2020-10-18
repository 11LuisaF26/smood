# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime as dt, timedelta
import logging

logger = logging.getLogger(__name__)


class TwitterConn:
    """
    Esta clase es usada para hacer conexiones a la API V2 de twitter.
    :Bearer access_token: Parametro necesario para hacer conexiones seguras 
    """

    def __init__(self, access_token):
        self.access_token = access_token

    def obtener_twiiter_user(self, nombre_usuario):
        """
        Este metodo utilizado para obtener tweets utilizando un username
        :nombre_usuario: Nombre de usuario sobre el que se va a hacer la peticion
        :return: Objeto response con los data de los tweets del usuario.
        """

        endpoint = "https://api.twitter.com/2/tweets/search/recent"


        payload = {
            "tweet.fields": "author_id,context_annotations,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld",
            "expansions": "referenced_tweets.id",
            "query": f"from:{nombre_usuario}"
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url=endpoint, params=payload, headers=headers)
        
        logger.error(response)

        return response
    
    def obtener_twiiter_query(self, query):
        """
        Este metodo utilizado para obtener tweets utilizando un query que es un string
        :query: String por la que se buscan los tweets
        :return: Objeto response con los data de los tweets de interes.
        """

        endpoint = "https://api.twitter.com/2/tweets/search/recent"

        payload = {
            "tweet.fields": "author_id,context_annotations,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,source,text,withheld",
            "expansions": "referenced_tweets.id",
            "query": query
        }

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url=endpoint, params=payload, headers=headers)
        
        logger.error(response)

        return response
