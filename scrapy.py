from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import pandas as pd

# Configurar Chrome (sin modo headless para ver lo que hace)
options = Options()
options.add_argument("--disable-notifications")

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL de la cartelera
URL = "https://www.filmaffinity.com/es/cat_new_th_es.html"
driver.get(URL)
print("✅ Página cargada correctamente")
time.sleep(3)  # Esperar a que todo cargue

# Buscar todos los enlaces a películas
print("Buscando películas...")
movie_links = []
all_links = driver.find_elements(By.TAG_NAME, "a")

for link in all_links:
    try:
        href = link.get_attribute("href")
        if href and "/es/film" in href and href not in movie_links:
            movie_links.append(href)
    except:
        continue

print(f"✅ Encontradas {len(movie_links)} películas")

# Lista para almacenar los datos
movie_data = []

# Procesar películas (limitamos a 10 para este ejemplo)
for idx, movie_link in enumerate(movie_links[:10]):
    try:
        print(f"Procesando película {idx+1}/10: {movie_link}")
        driver.get(movie_link)
        time.sleep(2)  # Esperar a que cargue la página
        
        # Diccionario para esta película
        movie_info = {
            "Película": "No disponible",
            "fecha_estreno": "No disponible",
            "sinopsis": "No disponible",
            "resenas": "No disponible"
        }
        
        # Obtener título
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, "h1[itemprop='name']")
            movie_info["Película"] = title_element.text.strip()
        except:
            # Intento alternativo para el título
            try:
                title_element = driver.find_element(By.CSS_SELECTOR, "h1.movie-title")
                movie_info["Película"] = title_element.text.strip()
            except:
                pass
        
        # Obtener fecha de estreno
        try:
            # Buscar todos los elementos dt (etiquetas de descripción)
            dt_elements = driver.find_elements(By.TAG_NAME, "dt")
            for dt in dt_elements:
                # Si encontramos el que dice "Estreno"
                if "estreno" in dt.text.lower():
                    # Obtenemos el siguiente elemento dd (que contiene la fecha)
                    next_dd = dt.find_element(By.XPATH, "./following-sibling::dd[1]")
                    movie_info["fecha_estreno"] = next_dd.text.strip()
                    break
        except:
            pass
        
        # Obtener sinopsis
        try:
            synopsis_element = driver.find_element(By.CSS_SELECTOR, "dd[itemprop='description']")
            movie_info["sinopsis"] = synopsis_element.text.strip()
        except:
            try:
                synopsis_element = driver.find_element(By.CSS_SELECTOR, "dd.text-large")
                movie_info["sinopsis"] = synopsis_element.text.strip()
            except:
                pass
        
        # Obtener reseñas (máximo 3)
        try:
            review_elements = driver.find_elements(By.CSS_SELECTOR, "div.review-text")
            if review_elements:
                resenas = []
                for i, review in enumerate(review_elements[:3]):
                    resenas.append(review.text.strip())
                movie_info["resenas"] = " | ".join(resenas)
        except:
            pass
        
        # Añadir esta película a nuestra lista
        movie_data.append(movie_info)
        print(f"✅ Información guardada para: {movie_info['Película']}")
        
    except Exception as e:
        print(f"Error con esta película: {e}")

# Cerrar el navegador
driver.quit()

# Guardar los datos en CSV
with open("peliculas_filmaffinity.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["Película", "fecha_estreno", "sinopsis", "resenas"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for data in movie_data:
        writer.writerow(data)

# Crear DataFrame para visualizar los resultados
df = pd.DataFrame(movie_data)
print("\n--- Películas extraídas ---")
print(df[["Película", "fecha_estreno"]])
print(f"\n✅ Datos guardados en peliculas_filmaffinity.csv")