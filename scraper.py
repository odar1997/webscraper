from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import pandas as pd
import sqlite3


con = sqlite3.connect('peliculas.db')
cur = con.cursor()
print("✅ Creando base de datos")
df = pd.read_csv("cartelera.csv")
print(df)


# Configurar Chrome en modo headless
options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL de la cartelera
URL = "https://www.filmaffinity.com/es/cat_new_th_es.html"
driver.get(URL)
print("✅ Página cargada correctamente")

# Buscar películas en la cartelera
movies = driver.find_elements(By.CLASS_NAME, "movie-poster")
data = []
# Crear archivo CSV para guardar datos
with open("cartelera.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Película", "fecha_estreno"])

    for movie in movies:
        info = movie.text.split("\n")
        title = info[2]
        fecha_estreno = info[0] + " " + info[1]
         #Buscar formatos (IMAX, 3D, etc.)
        
        data.append([title, fecha_estreno])

        writer.writerow([title, fecha_estreno])
        print(f"🎬 {title} - {fecha_estreno}")

cur.execute("create table if not exists cartelera (title UNIQUE, fecha_estreno)")


cur.executemany("INSERT OR IGNORE INTO cartelera VALUES(?, ?)", data)
con.commit()
print("✅ Datos guardados en la base de datos")

driver.quit()
print("✅ Datos guardados en cartelera.csv")


