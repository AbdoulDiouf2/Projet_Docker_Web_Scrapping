import scrapy
from headphones_scraper.items import HeadphoneItem
from datetime import datetime

class BoulangerSpider(scrapy.Spider):
    name = 'boulanger'
    allowed_domains = ['boulanger.com']
    start_urls = ['https://www.boulanger.com/nav/recherche?text=casque']

    def parse(self, response):
        # Exemple de structure, à adapter selon le site
        for product in response.css('.product-item'):
            item = HeadphoneItem()
            
            item['source_website'] = 'boulanger.com'
            item['scrape_timestamp'] = datetime.now().isoformat()
            
            item['brand'] = product.css('.brand::text').get()
            item['model'] = product.css('.model::text').get()
            item['full_name'] = product.css('.product-name::text').get()
            
            # Prix
            item['current_price'] = product.css('.price::text').get()
            
            # URL
            item['product_url'] = product.css('a::attr(href)').get()
            
            yield item
        
        # Pagination
        next_page = response.css('.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
