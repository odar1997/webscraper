from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import pandas as pd
import traceback
import os

# Configurar Chrome (sin headless para depuración)
options = Options()
# options.add_argument("--headless")  # Descomentado para ver el navegador en acción
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-notifications")

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL de la cartelera
URL = "https://www.filmaffinity.com/es/cat_new_th_es.html"

try:
    driver.get(URL)
    print("✅ Página cargada correctamente")
    time.sleep(5)  # Esperar a que todo cargue
    
    # Manejar cookies si aparece el diálogo
    try:
        cookie_buttons = driver.find_elements(By.CSS_SELECTOR, "button.qc-cmp2-button")
        for button in cookie_buttons:
            if "acepto" in button.text.lower() or "aceptar" in button.text.lower() or "accept" in button.text.lower():
                button.click()
                print("✅ Cookies aceptadas")
                time.sleep(2)
                break
    except Exception as e:
        print(f"Nota sobre cookies: {e}")
    
    # Obtener todos los enlaces a películas
    print("Buscando enlaces a películas...")
    movie_links = []
    
    # Método 1: Buscar enlaces directamente
    all_links = driver.find_elements(By.TAG_NAME, "a")
    for link in all_links:
        try:
            href = link.get_attribute("href")
            if href and "/es/film" in href and href not in movie_links:
                movie_links.append(href)
        except:
            continue
    
    print(f"✅ Encontrados {len(movie_links)} enlaces a películas")
    
    # Guardar los enlaces para referencia y depuración
    with open("movie_links.txt", "w", encoding="utf-8") as f:
        for link in movie_links:
            f.write(f"{link}\n")
    print("✅ Enlaces guardados en movie_links.txt")
    
    # Lista para almacenar los datos de las películas
    movie_data = []
    
    # Limitar a 10 películas para pruebas (aumenta según necesites)
    limit = 10
    for idx, movie_link in enumerate(movie_links[:limit]):
        try:
            print(f"\n--- Procesando película {idx+1}/{limit} ---")
            print(f"🔗 Visitando: {movie_link}")
            
            driver.get(movie_link)
            time.sleep(3)  # Esperar a que cargue la página
            
            # Diccionario para almacenar los datos de esta película
            movie_info = {
                "Película": "No disponible",
                "fecha_estreno": "No disponible",
                "sinopsis": "No disponible",
                "resenas": "No disponible"
            }
            
            # Obtener título (probando varios métodos)
            try:
                title_selectors = [
                    "h1[itemprop='name']",
                    "h1.movie-title",
                    "h1.header-title",
                    "#main-title"
                ]
                
                for selector in title_selectors:
                    title_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if title_elements:
                        movie_info["Película"] = title_elements[0].text.strip()
                        print(f"✅ Título: {movie_info['Película']}")
                        break
            except Exception as e:
                print(f"❌ Error obteniendo título: {e}")
            
            # Obtener fecha de estreno
            try:
                date_selectors = [
                    "dd.release",
                    "dd[itemprop='datePublished']",
                    "dd:contains('Estreno')"
                ]
                
                for selector in date_selectors:
                    try:
                        date_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if date_elements:
                            movie_info["fecha_estreno"] = date_elements[0].text.strip()
                            print(f"✅ Fecha de estreno: {movie_info['fecha_estreno']}")
                            break
                    except:
                        continue
                
                # Si no encontramos la fecha con los selectores, buscamos por texto
                if movie_info["fecha_estreno"] == "No disponible":
                    all_dt = driver.find_elements(By.TAG_NAME, "dt")
                    for dt in all_dt:
                        if "estreno" in dt.text.lower():
                            next_dd = dt.find_element(By.XPATH, "./following-sibling::dd[1]")
                            if next_dd:
                                movie_info["fecha_estreno"] = next_dd.text.strip()
                                print(f"✅ Fecha de estreno (método alternativo): {movie_info['fecha_estreno']}")
                                break
            except Exception as e:
                print(f"❌ Error obteniendo fecha de estreno: {e}")
            
            # Obtener sinopsis
            try:
                synopsis_selectors = [
                    "dd[itemprop='description']",
                    "dd.text-large",
                    "div.plot",
                    "div.synopsis",
                    "dd.description"
                ]
                
                for selector in synopsis_selectors:
                    synopsis_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if synopsis_elements:
                        movie_info["sinopsis"] = synopsis_elements[0].text.strip()
                        print(f"✅ Sinopsis obtenida ({len(movie_info['sinopsis'])} caracteres)")
                        break
            except Exception as e:
                print(f"❌ Error obteniendo sinopsis: {e}")
            
            # Obtener reseñas
            try:
                review_selectors = [
                    "div.review-text",
                    "div[itemprop='reviewBody']",
                    ".user-reviews-wrapper p",
                    "div.comment-text"
                ]
                
                resenas = []
                for selector in review_selectors:
                    review_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    if review_elements:
                        for i, review in enumerate(review_elements[:3]):  # Limitamos a 3 reseñas
                            resena_texto = review.text.strip()
                            if resena_texto:
                                resenas.append(resena_texto)
                        
                        if resenas:
                            print(f"✅ Obtenidas {len(resenas)} reseñas")
                            movie_info["resenas"] = " | ".join(resenas)
                            break
            except Exception as e:
                print(f"❌ Error obteniendo reseñas: {e}")
            
            # Guardar los datos de esta película
            movie_data.append(movie_info)
            
            # Tomar una captura de pantalla para depuración (opcional)
            os.makedirs("capturas", exist_ok=True)
            driver.save_screenshot(f"capturas/pelicula_{idx+1}.png")
            
        except Exception as e:
            print(f"Error procesando película {idx+1}: {str(e)}")
            traceback.print_exc()
    
    # Guardar todos los datos recopilados
    if movie_data:
        # Guardar en CSV
        with open("cartelera_completa.csv", "w", newline="", encoding="utf-8") as file:
            fieldnames = ["Película", "fecha_estreno", "sinopsis", "resenas"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for data in movie_data:
                writer.writerow(data)
        
        # Mostrar resumen
        df = pd.DataFrame(movie_data)
        print("\n--- Películas extraídas ---")
        for idx, row in df.iterrows():
            title = row["Película"] if row["Película"] != "No disponible" else f"Película {idx+1}"
            fecha = row["fecha_estreno"]
            has_synopsis = "Sí" if row["sinopsis"] != "No disponible" else "No"
            has_reviews = "Sí" if row["resenas"] != "No disponible" else "No"
            
            print(f"{idx+1}. {title} | Fecha: {fecha} | Sinopsis: {has_synopsis} | Reseñas: {has_reviews}")
        
        print(f"\n✅ Datos de {len(movie_data)} películas guardados en cartelera_completa.csv")
    else:
        print("❌ No se encontraron datos de películas para guardar")

except Exception as e:
    print(f"Error general: {str(e)}")
    traceback.print_exc()
finally:
    # Cerrar el navegador
    driver.quit()
    print("✅ Navegador cerrado")