En este repositorio se encuentran los códigos de nuestro proyecto, app.py, Database.py y robots.html

Database.py tiene todos los metodos que editan la base de datos añadiendo eliminando o modificando datos para diferentes tablas.

app.py es el puente entre la base de datos y el html, contiene metodos que referencian a Database.py. Mediante Flask crea un servidor localhost con el que puede leer y escribir datos.

robots.html es la interfaz gráfica para ejecutar directamente los metodos de Database.py
