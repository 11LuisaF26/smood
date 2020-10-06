from background_task import background
from django.contrib.auth.models import User
from facebook_scraper import get_posts
from app.models import data_red
import logging
logger = logging.getLogger(__name__)

@background(schedule=5)
def get_facebook_post(nombre_pagina, numero_paginas):
    for publicacion in get_posts(nombre_pagina, pages=numero_paginas):
        if publicacion:
            publicacion_id = publicacion["post_id"]
            publicacion_texto = publicacion["post_text"][:50]
            publicacion_fecha = publicacion["time"]
            publicacion_likes = publicacion["likes"]
            publicacion_comentarios = publicacion["comments"]
            publicacion_compartidos = publicacion["shares"]
            publicacion_user = publicacion["user_id"]

            d = data_red(
                        publicacion_id = publicacion_id, 
                        publicacion_fecha = publicacion_texto,
                        publicacion_texto = publicacion_fecha, 
                        publicacion_likes = publicacion_likes,
                        publicacion_comentarios = publicacion_comentarios,
                        publicacion_compartidos = publicacion_compartidos,
                        publicacion_user = publicacion_user
                )
            d.save()

        else:
            logger.error("Ha ocurrido un error")
