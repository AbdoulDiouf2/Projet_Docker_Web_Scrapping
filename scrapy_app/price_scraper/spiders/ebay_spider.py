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