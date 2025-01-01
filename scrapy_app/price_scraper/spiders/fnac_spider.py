
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..items import ProductItem  # Import de l'item
import time

class CdiscountSpider(scrapy.Spider):
    name = "cdiscount"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuration Selenium
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def start_requests(self):
        # Définir l'URL de départ
        urls = ['https://www.cdiscount.com/search/10/casques.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)

        while True:
            try:
                # Extraction des articles sur la page actuelle
                articles = self.driver.find_elements(By.XPATH, '//li[@class="abLabel"]')

                for article in articles:
                    try:
                        item = ProductItem()

                        # Extraire les données de chaque article
                        item['site_name'] = "Cdiscount"
                        item['price'] = article.find_element(By.XPATH, './/span[@class="priceColor price"]').text + \
                                        article.find_element(By.XPATH, './/span[@class="priceColor price"]/sup').text
                        item['name'] = article.find_element(By.XPATH, './/h2[@class="alt-h4 u-line-clamp--2"]').text
                        item['image_url'] = article.find_element(By.XPATH, './/img[@class="prdtBImg"]').get_attribute('src')
                        item['product_url'] = article.find_element(By.XPATH, './/a[@class="jsPrdtBILA prdtBILA"]').get_attribute('href')

                        # Envoyer l'article au pipeline
                        yield item

                    except Exception as e:
                        self.logger.error(f"Erreur lors de l'extraction de l'article : {e}")

                # Trouver et cliquer sur le bouton "Page suivante"
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[contains(@class, "jsNxtPage")]'))
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)  # Délai pour éviter les erreurs
                next_button.click()

                # Attendre que la page suivante charge ses articles
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//li[@class="abLabel"]'))
                )

            except Exception as e:
                self.logger.info(f"Fin des pages ou erreur : {e}")
                break

    def closed(self, reason):
        self.driver.quit()  