from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# Configurar Chrome en modo headless
options = Options()
# Comentamos el modo headless para poder ver qué está pasando (si es posible)
# options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

# Inicializar WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL de la cartelera
URL = "https://www.filmaffinity.com/es/cat_new_th_es.html"
driver.get(URL)
print("✅ Página cargada correctamente")

# Añadir una pausa para asegurarnos de que la página carga completamente
time.sleep(5)

# Vamos a imprimir el HTML de la página para ver su estructura
page_source = driver.page_source
print("Estructura de la página:")
print(page_source[:1000])  # Imprimir los primeros 1000 caracteres para ver la estructura

# Intentar encontrar elementos con diferentes clases comunes para películas
try:
    # Intentar con diferentes selectores posibles
    selectors_to_try = [
        "movie-card", "movie-poster", "movie-title", "movie-item", 
        "movie", "fa-movie", "fa-shadow", "movie-tit", "movie-rating",
        "fa-frame-wrapper", "movie-card-1"
    ]
    
    for selector in selectors_to_try:
        elements = driver.find_elements(By.CLASS_NAME, selector)
        print(f"Elementos con clase '{selector}': {len(elements)}")
    
    # También intentar con etiquetas comunes que podrían contener películas
    divs = driver.find_elements(By.TAG_NAME, "div")
    print(f"Total de divs en la página: {len(divs)}")
    
    # Intentar encontrar los elementos por XPath más general
    movie_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'mov')]")
    print(f"Elementos que contienen 'mov' en su clase: {len(movie_elements)}")
    
except Exception as e:
    print(f"❌ Error al buscar elementos: {e}")

# Cerrar el navegador
driver.quit()
print("✅ Navegador cerrado")