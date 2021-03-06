<h1 align="center" color="blue">Universidad de Bogotá Jorge Tadeo Lozano</H1>

<p align="center">
  <img src="https://i.pinimg.com/originals/ae/06/64/ae06647022c506cd7541fec434f607ad.jpg" />
</p>

<h1 align="center" color="blue">SMOOD - Software de planeación estratégica </H1>

## ¿Qué es S-mood?
Es un software piloto para la automatización de la construcción de la variable de Comunicación en modelo semiótico de cuatro variables.

## ¿Por qué S-mood?
Al ser el resultado de la fusión de la investigación de mercados y la planeación estratégica publicitaria,
se propone el nombre S-mood para el software.  
Para llegar a él se parte de las dos palabras “Semiotic” y “Model”, 
pero se realizan  combinaciones de términos como  La S de semiótica y 
se le agrega una “o” a la palabra “model” con lo cual se gana sonoridad, 
pero además se agrega la significación de Mood del “humor” como estado de animo.  
Al final, la combinación implica el estudio del estado de ánimo, 
los comportamientos de las personas y las estrategias que de allí 
se pueden generar para resolver casos de Publicidad y de Marketing, 
el cual es el objetivo principal de la Investigación y del Software.

![GitHub Logo](/core/static/assets/images/1logo.png)


## Requisitos
* python 3
* virtualenv
* requirements.txt.

## ¿Cómo usarlo?

```bash
$ # Obtener el código
$ git clone https://github.com/11LuisaF26/smood.git
$ cd smood
$
$ # Virtualenv (Para sistemas Unix)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv (Para sistemas Windows)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Instalar las dependencias necesarias
$ pip3 install -r requirements.txt
$
$ # Crear tablas
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Cargar datos para el funcionamiento en las modelos: red_social y estado_empresa
$ python manage.py loaddata data.json
$
$ # Iniciar la aplicación (Modo de desarrollo)
$ python manage.py runserver # Puerto por defecto 8000
```

> Nota: Para usar la aplicación es necesario registrar un nuevo usuario, después de esto la aplicación desbloqueará las vistas privadas.

<br />

## Estructura base del código

El proyecto usa la siguiente estructura:

```bash
< PROJECT ROOT >
   |
   |-- core/
   |    |-- settings.py
   |    |-- wsgi.py
   |    |-- urls.py
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>
   |    |
   |    |-- templates/
   |         |
   |         |-- includes/
   |         |    |-- navigation.html
   |         |    |-- sidebar.html
   |         |    |-- footer.html
   |         |    |-- scripts.html
   |         |
   |         |-- layouts/
   |         |    |-- base-fullscreen.html
   |         |    |-- base.html
   |         |
   |         |-- accounts/
   |         |    |-- login.html
   |         |    |-- register.html
   |         |
   |      index.html
   |     page-404.html
   |     page-500.html
   |       *.html
   |
   |-- authentication/
   |    |
   |    |-- urls.py
   |    |-- views.py
   |    |-- forms.py
   |
   |-- app/
   |    |
   |    |-- views.py
   |    |-- urls.py
   |    |-- test.py
   |    |-- forms.py
   |    |-- models.py
   |    |-- nube.py
   |    |-- tasks.py
   |    |-- twitter_conn.py
   |
   |-- requirements.txt
   |
   |-- .env
   |-- manage.py
   |
   |-- ************************************************************************
```
<br />

## AUTORES 

*   Olmer Garcia Bedoya 
*   Victor Danilo Castañeda Pinzón
*   Luisa Fernanda Rodriguez Sarmiento

    ###  CONTRIBUYENTES
    *   Isabel Sofía Enriquez Avilez
    *   Vladimir Sánchez Riaño
    *   Gabriela Andrade Caicedo
    *   Catherine Suarez Báez
	  *	  Jairo Sojo