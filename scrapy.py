from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# Configurar Chrome
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL de la cartelera
URL = "https://www.filmaffinity.com/es/cat_new_th_es.html"
driver.get(URL)
print("✅ Página cargada correctamente")

# Esperar a que la página cargue
time.sleep(5)

# Crear lista para almacenar datos
peliculas_data = []

try:
    # Intentemos un enfoque diferente: buscar directamente los elementos título
    titulos = driver.find_elements(By.CLASS_NAME, "movie-title")
    print(f"Se encontraron {len(titulos)} títulos de películas")
    
    for titulo_element in titulos:
        try:
            # Obtener el título
            titulo = titulo_element.text.strip()
            
            # Obtener el año - está en un elemento cercano
            anio = "No disponible"
            # El elemento padre contiene ambos título y año
            parent = titulo_element.find_element(By.XPATH, "..")  # Obtener elemento padre
            try:
                year_element = parent.find_element(By.CLASS_NAME, "year")
                anio = year_element.text.strip()
            except:
                # Intenta buscar en elementos cercanos
                try:
                    # A veces el año está en un elemento hermano
                    year_element = parent.find_element(By.XPATH, "following-sibling::div[contains(@class, 'year')]")
                    anio = year_element.text.strip()
                except:
                    # Si todo falla, buscar cualquier elemento con clase 'year' cercano
                    try:
                        year_element = titulo_element.find_element(By.XPATH, "../..//div[contains(@class, 'year')]")
                        anio = year_element.text.strip()
                    except:
                        pass
            
            # Guardar datos si tenemos al menos el título
            if titulo:
                peliculas_data.append([titulo, anio])
                print(f"Película encontrada: {titulo} ({anio})")
        
        except Exception as e:
            print(f"Error al procesar una película: {str(e)}")
    
    # Si no encontramos títulos, intentar otro enfoque
    if len(peliculas_data) == 0:
        print("Intentando otro método para encontrar películas...")
        # Obtener todos los divs que contienen la clase 'movie-poster'
        movie_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'movie-poster')]")
        
        for movie in movie_elements:
            try:
                # Obtener el contenedor de la película (subiendo niveles)
                movie_container = movie.find_element(By.XPATH, "../..")
                
                # Imprimir el HTML para diagnóstico
                html = movie_container.get_attribute("outerHTML")
                print(f"HTML de película: {html[:100]}...")  # Mostrar parte del HTML
                
                # Intentar encontrar el título y año
                titulo = "No disponible"
                anio = "No disponible"
                
                # Buscar el título en cualquier elemento con clase que contenga 'title'
                try:
                    titulo_element = movie_container.find_element(By.XPATH, ".//a[contains(@class, 'title')]")
                    titulo = titulo_element.text.strip()
                except:
                    # Intentar con otros selectores comunes
                    try:
                        titulo_element = movie_container.find_element(By.XPATH, ".//a")
                        titulo = titulo_element.text.strip()
                    except:
                        pass
                
                # Buscar el año
                try:
                    year_element = movie_container.find_element(By.XPATH, ".//div[contains(@class, 'year')]")
                    anio = year_element.text.strip()
                except:
                    pass
                
                # Guardar solo si tenemos un título
                if titulo != "No disponible" and titulo:
                    peliculas_data.append([titulo, anio])
                    print(f"Película encontrada (método 2): {titulo} ({anio})")
            
            except Exception as e:
                print(f"Error en método 2: {str(e)}")
    
    # Si seguimos sin encontrar títulos, tomar una captura para diagnóstico
    if len(peliculas_data) == 0:
        print("Guardando captura de pantalla para diagnóstico...")
        driver.save_screenshot("filmaffinity_debug.png")
        print("Captura guardada como 'filmaffinity_debug.png'")
    
    # Guardar en CSV
    with open("cartelerapelis.csv", 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Título", "Año"])
        csv_writer.writerows(peliculas_data)
    
    print(f"✅ Se han guardado {len(peliculas_data)} películas en cartelerapelis.csv")

except Exception as e:
    print(f"Error general: {str(e)}")

# Cerrar el navegador
driver.quit()
print("✅ Navegador cerrado")