S-MOOD

¿QUÉ ES S-MOOD?
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

PREREQUISITOS
Gracias a las herramientas que se utilizan en el software, el cual podemos decir estan basadas o 
por defecto trabajan en base a el sistema operativo Linux. Se recomienda que para poder ejecutar
el software de manera correcta en una maquina local, lo mejor es trabajar en un sistema operativo 
a base de Linux. Para el sistema operativo Windows, vimos reflejados varios inconvenientes de 
compatibilidad, y por lo tanto para este escenario se llegó a la conclusión que, la opción más óptima es 
instalar el subsistema de Windows para Linux, de esta forma evitamos diferentes tipos de errores que el 
sistema Windows nos arroja. 

A continuación se mencionan los programas que deben ser instalados antes, para una instalación correcta 
del software:

Git 				--- 	https://git-scm.com/downloads
Python 				--- 	https://www.python.org/downloads/
Subsistema Linux 	--- 	Windows 10 trae la opción de habilitar el subsistema Linux desde configuraciones,
							acá encuentra la guía  https://docs.microsoft.com/es-es/windows/wsl/install-on-server
Ubuntu 				---		Una vez instalado el subsistema, ya se puede descargar la aplicación de Ubuntu desde 
							la Microsoft Store

Las dependencias se pueden encontrar en el archivo requirements.txt. 
En el siguiente item se encontraran los pasos para su correcta instalación.

INSTALACIÓN
1. Clonar el repositorio de GITHUB
	git clone https://github.com/11LuisaF26/smood
	cd smood
	
2. Crear entorno virtual 
	python -m venv env

3. Instalar requirements.txt	
	pip3 install -r requirements.txt

4. Hacer las migraciones		
	python manage.py makemigrations
	python manage.py migrate

5. Iniciar la aplicación	
	python manage.py runserver

6. Crear super usuario
	python manage.py createsuperuser

CONSTRUIDO CON
- Python
- Django
- PostgreSQL

AUTORES
-   Olmer Garcia Bedoya 
-   Victor Danilo Castañeda Pinzón
-   Luisa Fernanda Rodriguez Sarmiento

    CONTRIBUYENTES
    -   Isabel Sofía Enriquez Avilez
    -   Vladimir Sánchez Riaño
    -   Gabriela Andrade Caicedo
    -   Catherine Suarez Báez
	-	Jairo Sojo
    
    