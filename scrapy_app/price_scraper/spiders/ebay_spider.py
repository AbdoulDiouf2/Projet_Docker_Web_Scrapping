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