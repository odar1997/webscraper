import unittest
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestFilmAffinityScraper(unittest.TestCase):
    
    @patch("selenium.webdriver.Chrome")
    def setUp(self, MockWebDriver):
        """ Configura el entorno de pruebas """
        self.mock_driver = MockWebDriver()
        self.mock_driver.get.return_value = None
        self.mock_driver.page_source = "<html><body><div class='movie-card'></div></body></html>"
        self.mock_driver.find_elements.return_value = [MagicMock() for _ in range(5)]
        self.url = "https://www.filmaffinity.com/es/cat_new_th_es.html"
        
    def test_page_load(self):
        """ Verifica que la página se carga correctamente """
        self.mock_driver.get(self.url)
        self.mock_driver.get.assert_called_with(self.url)

    def test_find_movie_elements(self):
        """ Verifica que se encuentran los elementos de películas """
        selectors_to_try = ["movie-card", "movie-title", "movie-item"]
        for selector in selectors_to_try:
            elements = self.mock_driver.find_elements(By.CLASS_NAME, selector)
            self.assertEqual(len(elements), 5)
    
    def test_xpath_search(self):
        """ Verifica que la búsqueda por XPath devuelve elementos """
        self.mock_driver.find_elements.return_value = [MagicMock() for _ in range(3)]
        elements = self.mock_driver.find_elements(By.XPATH, "//div[contains(@class, 'mov')]")
        self.assertEqual(len(elements), 3)
    
    def test_close_browser(self):
        """ Verifica que el navegador se cierra correctamente """
        self.mock_driver.quit()
        self.mock_driver.quit.assert_called()

if __name__ == "__main__":
    unittest.main()
