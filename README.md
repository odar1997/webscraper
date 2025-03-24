# webscraper
recoleccion de datos de una pagina 
Este proyecto es para los cinefilos y mi base de lo que queria lograr era scrapear la pagina de cinesa que es la que uso normalmente y queria los datos para tener la informacion de las peliculas y horarios ya que todo buen fanatico le gusta verlo en idioma original y en españa casi siempre la mayoria de las peliculas estan dobladas y queria abordar este problema 

# realizando el scraper
al intentar scrapear la pagina de cinesa no me dejo y daba error entonces opte por irme a otra pagina la de kinetpolis y esta me bloqueo incluso entonces busque paginas mas sencillas a ver si quizas lo lograba hasta que llegue a la de filmaffinity que me salvo la vida 

# 🎬 Scraper de Cartelera de Películas con Selenium

Este script usa `Selenium` para extraer los **títulos** y **fechas de estreno** de las películas en la cartelera de [FilmAffinity](https://www.filmaffinity.com/es/cat_new_th_es.html) y guardarlos en un archivo CSV.

---

## 🚀 Instalación y Requisitos

### 📌 **1. Instalar Python**
Asegúrate de tener Python 3 instalado en tu sistema.  
Para verificarlo, ejecuta en la terminal o línea de comandos:

sh
python --version
´´´´
##instalar dependencias
pip install selenium webdriver-manager pandas

 Descripción de las librerías usadas en el script:

selenium → Permite automatizar la navegación en sitios web.
webdriver-manager → Administra la descarga y actualización del controlador de Chrome.
pandas → Permite manejar archivos CSV de forma sencilla

📜 Funcionamiento del Script
1️⃣ Inicialización del navegador con Selenium

Se configura Chrome en modo headless (sin abrir una ventana visual).
Se deshabilita la GPU y se establece un tamaño de ventana de 1920x1080.
2️⃣ Carga de la página de FilmAffinity

Se accede a la URL de la cartelera de estrenos:
👉 https://www.filmaffinity.com/es/cat_new_th_es.html
3️⃣ Extracción de datos

Se buscan los elementos que contienen los títulos y fechas de estreno de las películas.
Se usa la función find_elements() con By.CLASS_NAME para ubicar los datos dentro del HTML.
4️⃣ Almacenamiento en un archivo CSV

Se crea (o sobrescribe) el archivo cartelera.csv.
Se escriben los datos extraídos en formato Película, Fecha de Estreno.
5️⃣ Cierre del navegador

Una vez extraída la información, el script cierra el navegador para liberar recursos.
6️⃣ Lectura del CSV y visualización de los datos

Se usa pandas para leer el archivo cartelera.csv y mostrar su contenido en la terminal.
▶️ Ejecución del Script
Para ejecutar el script, simplemente abre la terminal en la carpeta del proyecto y escribe:

## Agregando base de datos con SQLite
import sqlite 
 = sqlite3.connect('peliculas.db')
cur = con.cursor()

siguiendo esos pasos se agrega luego esta parte del codigo 

cur.execute("create table if not exists cartelera (title UNIQUE, fecha_estreno)")


cur.executemany("INSERT OR IGNORE INTO cartelera VALUES(?, ?)", data)
con.commit()

## Test Unitarios 
tengo test unitarios en una de las ramas la cual llame sin complicarme mucho solo "test" pienso agregar un test  mi rama principal  

## RAMAS 
pueden ver y los invitos a ver mis otras ramas ya que es un poco mas avanzado el codigo pero decidi no incluirla a la principal pero las ramas estan y existen son nmain(Que es la que estamos) dev,super/code, data/base ,test

## Trello
aca les dejo tambien la conexion de mi trello [https://trello.com/b/xq6pXNWV/web-scraping]



## Correr el programa
python scraper.py
