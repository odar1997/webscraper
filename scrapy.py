from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv

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

# Esperar a que los elementos de las películas estén disponibles
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "movie-card"))
    )
    print("✅ Elementos de películas cargados")
except Exception as e:
    print(f"❌ Error al cargar los elementos: {e}")
    driver.quit()
    exit()

# Buscar películas en la cartelera (cada película está en un div con clase movie-card)
movies = driver.find_elements(By.CLASS_NAME, "movie-card")
print(f"🎥 Se encontraron {len(movies)} películas")

# Crear archivo CSV para guardar datos
with open("cartelera.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Película", "Fecha Estreno", "Director", "Reparto", "Valoración"])

    for movie in movies:
        try:
            # Obtener título
            title_element = movie.find_element(By.CLASS_NAME, "mc-title").find_element(By.TAG_NAME, "a")
            title = title_element.text.strip()
            
            # Obtener fecha de estreno (está en un div con clase mc-date)
            try:
                fecha_estreno = movie.find_element(By.CLASS_NAME, "mc-date").text.strip()
            except:
                fecha_estreno = "Fecha no disponible"
                
            # Obtener director
            try:
                director = movie.find_element(By.CLASS_NAME, "mc-director").text.strip()
            except:
                director = "Director no disponible"
                
            # Obtener reparto
            try:
                reparto = movie.find_element(By.CLASS_NAME, "mc-cast").text.strip()
            except:
                reparto = "Reparto no disponible"
                
            # Obtener valoración
            try:
                valoracion = movie.find_element(By.CLASS_NAME, "avgrat-box").text.strip()
            except:
                valoracion = "Sin valoración"

            # Escribir en el archivo CSV
            writer.writerow([title, fecha_estreno, director, reparto, valoracion])
            print(f"🎬 {title} - {fecha_estreno}")
        except Exception as e:
            print(f"❌ Error al procesar una película: {e}")

driver.quit()
print("✅ Datos guardados en cartelera.csv")