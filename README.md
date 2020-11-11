<h1 align="center" color="blue">SMOOD - Software de planeación estratégica </H1>

<p align="center">
  <img src="https://i.pinimg.com/originals/ae/06/64/ae06647022c506cd7541fec434f607ad.jpg" />
</p>


## ¿Cómo usarlo?

```bash
$ # Obtener el código
$ git clone https://github.com/app-generator/django-dashboard-gradientable.git
$ cd django-dashboard-gradientable
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
   |
   |-- requirements.txt
   |
   |-- .env
   |-- manage.py
   |
   |-- ************************************************************************
```
<br />

## Deployment

Esta aplicación provee una configuración báscia para ser ejecutada en: [Docker](https://www.docker.com/), [Gunicorn](https://gunicorn.org/), y[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

### [Docker](https://www.docker.com/)
---

La aplicación puede ser ejecutada siguiendo estos pasos:

> Obtener el código

```bash
$ git clone https://github.com/app-generator/django-dashboard-gradientable.git
$ cd django-dashboard-gradientable
```

> Iniciar la aplicación en Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visitar `http://localhost:5005` en el navegador. La aplicación debería estar lista para ser usada.

<br />

### [Gunicorn](https://gunicorn.org/)
---

Gunicorn 'Green Unicorn' es un servidor WSGI HTTP de Python para UNIX.

> Instalar usando pip

```bash
$ pip install gunicorn
```
> Iniciar la aplicación usando gunicorn binary

```bash
$ gunicorn --bind=0.0.0.0:8001 core.wsgi:application
Serivicio en http://localhost:8001
```

Visitar `http://localhost:8001` en el navegador. La aplicación debería estar lista para ser usada.


<br />

### [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)
---

Waitress es el Gunicorn equivalente para Windows

> Instalar usando pip

```bash
$ pip install waitress
```
> Iniciar la aplicación usando: [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html)

```bash
$ waitress-serve --port=8001 core.wsgi:application
Servicio en http://localhost:8001
```

Visitar `http://localhost:8001` en el navegador. La aplicación debería estar lista para ser usada.