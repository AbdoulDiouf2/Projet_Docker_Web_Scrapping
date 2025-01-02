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
 
class CdiscountSpider(scrapy.Spider):
    name = "CDiscount"
   
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
        # chrome_service = Service("/usr/bin/google-chrome")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(
            service = service,
            options=chrome_options
        )
       
        # Modifier les propriétés pour éviter la détection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'
        })
 
    def start_requests(self):
        urls = ['https://www.cdiscount.com/search/10/casques.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.ContentTypeId=16&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&TechnicalForm.BrandLicenseId=0&NavigationForm.CurrentSelectedNavigationPath=categorycodepath%2F13%7C1305%7C130501&NavigationForm.FirstNavigationLinkCount=3&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets%5B2%5D=Marque%2Fapple&FacetForm.SelectedFacets%5B2%5D=Marque%2Fasus&FacetForm.SelectedFacets%5B2%5D=Marque%2Fbeats&FacetForm.SelectedFacets%5B2%5D=Marque%2Fbose&FacetForm.SelectedFacets%5B2%5D=Marque%2Fjbl&FacetForm.SelectedFacets%5B2%5D=Marque%2Fsamsung&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=casques&ProductListTechnicalForm.TemplateName=InLine&&_his_']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        self.driver.get(response.url)
        self.logger.info("Page chargée : %s", response.url)
       
        # Attendre que la page soit complètement chargée
        time.sleep(5)
       
        try:
            # Test de différents sélecteurs pour les produits
            selectors = [
                '//div[contains(@class, "lpProducts")]//li',
                '//div[contains(@class, "product-list")]//div[contains(@class, "product")]',
                '//ul[contains(@class, "products-list")]//li',
                '//li[@class="abLabel"]'
            ]
           
            articles = []
            for selector in selectors:
                try:
                    articles = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, selector))
                    )
                    if articles:
                        self.logger.info(f"Sélecteur trouvé : {selector} avec {len(articles)} articles")
                        break
                except:
                    continue
 
            if not articles:
                self.logger.error("Aucun article trouvé")
                return
 
            for article in articles:
                try:
                    item = ProductItem()
                    item['site_name'] = "CDiscount"
                    item['scraped_at'] = datetime.now()
                   
                    # Nom (test multiple sélecteurs)
                    name_selectors = [
                        './/h2[@class="alt-h4 u-line-clamp--2"]',
                        './/h3[contains(@class, "productName")]',
                        './/div[contains(@class, "prdtTit")]'
                    ]
                    for selector in name_selectors:
                        try:
                            item['name'] = article.find_element(By.XPATH, selector).text
                            if item['name']:
                                break
                        except:
                            continue
                   
                    # Prix (test multiple sélecteurs)
                    try:
                        price = article.find_element(By.XPATH, './/*[contains(@class, "price")]').text
                        item['price'] = float(price.replace('€', '').replace(',', '.').strip())/100
                    except:
                        continue
                   
                    # URL et image
                    item['product_url'] = article.find_element(By.XPATH, './/a[1]').get_attribute('href')
                    item['image_url'] = article.find_element(By.XPATH, './/img').get_attribute('src')
 
                    # Description
                    features = article.find_elements(By.XPATH, './/*[contains(@class, "prdtBILDesc jsPrdtBILLink")]')
                    item['description'] = ' '.join([f.text.strip() for f in features if f.text.strip()])
                   
                    yield item
                   
                except Exception as e:
                    self.logger.error(f"Erreur lors de l'extraction de l'article : {e}")
 
            # Pagination
            current_page = response.meta.get('page', 1)
            if current_page < 10 and len(articles) > 0:
                next_page = current_page + 1
                base_url = ("https://www.cdiscount.com/search/10/casques.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.ContentTypeId=16&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&TechnicalForm.BrandLicenseId=0&NavigationForm.CurrentSelectedNavigationPath=categorycodepath%2F13%7C1305%7C130501&NavigationForm.FirstNavigationLinkCount=3&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets%5B0%5D=Marque%2Fapple&FacetForm.SelectedFacets%5B0%5D=Marque%2Fasus&FacetForm.SelectedFacets%5B0%5D=Marque%2Fbeats&FacetForm.SelectedFacets%5B0%5D=Marque%2Fbose&FacetForm.SelectedFacets%5B0%5D=Marque%2Fjbl&FacetForm.SelectedFacets%5B0%5D=Marque%2Fsamsung&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=9&FacetForm.SelectedFacets.Index=10&FacetForm.SelectedFacets.Index=11&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&FacetForm.SelectedFacets.Index=12&FacetForm.SelectedFacets.Index=13&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=casques&ProductListTechnicalForm.TemplateName=InLine"
                            f"&page={next_page}#_his_{next_page}")
               
                next_url = base_url
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