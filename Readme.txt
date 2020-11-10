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
Estos se pueden encontrar en el archivo requirements.txt. 
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
    
    