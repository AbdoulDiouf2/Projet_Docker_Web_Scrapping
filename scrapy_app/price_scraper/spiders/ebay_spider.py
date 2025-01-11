import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ..items import ProductItem
import time
from datetime import datetime
 
class EBaySpider(scrapy.Spider):
    name = "EBay"
   
    custom_settings = {
        'ITEM_PIPELINES': {
            'price_scraper.pipelines.MySQLPipeline': 300,
        }
    }
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuration Chrome
        chrome_options = Options()

                # Options pour éviter la détection
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
       
        # Activation du mode headless
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
 
        # User agent et autres options
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--lang=fr-FR')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Installation automatique du driver avec webdriver_manager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
       
        # Modifier les propriétés pour éviter la détection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        })
 
    def start_requests(self):
        urls = ['https://www.ebay.fr/sch/i.html?_dcat=112529&_fsrp=1&_from=R40&_nkw=ecouteur&_sacat=0&Marque=Philips%7CBose%7CASUS%7CApple%7CSamsung%7CJVC%7CJBL%7CJabra%7CBeat&rt=nc&LH_ItemCondition=1000']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        self.driver.get(response.url)
        self.logger.info("Page chargée : %s", response.url)
       
        # Attendre que la page soit complètement chargée
        time.sleep(5)
       
        # XPATH pour tous les produits : //ul[@class='srp-results srp-list clearfix']/li
        # XPath pour le nom : //ul[@class='srp-results srp-list clearfix']/li/div/div[2]/a/div/span/text()
        # XPath pour le prix : //ul[@class='srp-results srp-list clearfix']/li/div/div[2]/div[3]/div/div/span/text()
        # XPath pour l'URL du produit : //ul[@class='srp-results srp-list clearfix']/li/div/div[2]/a/@href
        # XPath pour l'image du produit : //ul[@class='srp-results srp-list clearfix']/li/div/div[1]/div/a/div/img/@src
        # Aperçu de la description --> "Neuf | Particulier"
        # XPath pour la description :
        # "Neuf" --> //ul[@class='srp-results srp-list clearfix']/li/div/div[2]/div[2]/span/text()
        # "Particulier --> //ul[@class='srp-results srp-list clearfix']/li/div/div[2]/div[2]/text()

        try:
            articles = self.driver.find_elements(By.XPATH, '//ul[@class="srp-results srp-list clearfix"]/li')
            if not articles:
                self.logger.error("Aucun article trouvé")
                return
 
            for article in articles:
                try:
                    item = ProductItem()
                    item['site_name'] = "eBay"
                    item['scraped_at'] = datetime.now()
                   
                    # Nom
                    item['name'] = article.find_element(By.XPATH, './/div/div[2]/a/div/span').text
                   
                    # Prix
                    price = article.find_element(By.XPATH, './/div/div[2]/div[3]/div/div/span').text
                    item['price'] = float(price.replace('EUR', '').replace(',', '.').strip())
                   
                    # URL et image
                    item['product_url'] = article.find_element(By.XPATH, './/div/div[2]/a').get_attribute('href')
                    item['image_url'] = article.find_element(By.XPATH, './/div/div[1]/div/a/div/img').get_attribute('src')
 
                    # Description
                    neuf = article.find_elements(By.XPATH, './/div/div[2]/div[2]/span')
                    particulier = article.find_elements(By.XPATH, './/div/div[2]/div[2]')
                    item['description'] = 'Neuf' if neuf else 'Particulier' if particulier else 'N/A'
                   
                    yield item
                   
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'extraction de l'article : {e}")

                # Pagination
            current_page = response.meta.get('page', 1)
            if current_page < 10 and len(articles) > 0:
                next_page = current_page + 1
                next_url = f"https://www.ebay.fr/sch/i.html?_dcat=112529&_fsrp=1&_from=R40&_nkw=ecouteur&_sacat=0&Marque=Philips%7CBose%7CASUS%7CApple%7CSamsung%7CJVC%7CJBL%7CJabra%7CBeat&rt=nc&LH_ItemCondition=1000&_pgn={next_page}"
                self.logger.info(f'Navigation vers la page suivante: {next_page}')
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse,
                    meta={'page': next_page}
                )
            elif current_page >= 10:
                self.logger.info("Limite de 10 pages atteinte, arrêt du scraping.")
            else:
                self.logger.info("Plus de produits trouvés, arrêt du scraping")
 
        except Exception as e:
            self.logger.error(f"Erreur générale : {e}")
 
    def closed(self, reason):
        if hasattr(self, 'driver'):
            self.driver.quit()