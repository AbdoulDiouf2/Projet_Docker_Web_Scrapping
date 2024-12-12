import scrapy
from datetime import datetime
from ..items import ProductItem

class BoulangerSpider(scrapy.Spider):
    name = 'boulanger'
    start_urls = ['https://www.boulanger.com/resultats?tr=casque']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def parse(self, response):
        # Utiliser le XPath pour obtenir tous les produits
        products = response.xpath("//ul/li[@class=' product-list__item']")
        self.logger.info(f'Found {len(products)} products')

        for product in products:
            try:
                item = ProductItem()
                
                # Nom du produit
                item['name'] = product.xpath(
                    ".//article/div[@class='product-list__product-area-2 g-col-5 g-col-sm-7 g-col-md-4 g-col-lg-3 g-col-xl-3']/a/h2/text()"
                ).get().strip()
                
                # URL du produit
                product_url = product.xpath(
                    ".//article/div[@class='product-list__product-area-2 g-col-5 g-col-sm-7 g-col-md-4 g-col-lg-3 g-col-xl-3']/a/@href"
                ).get()
                item['product_url'] = response.urljoin(product_url) if product_url else None

                # Prix
                price_str = product.xpath(
                    ".//article/div[@class='product-list__product-area-3 g-col-5 g-col-sm-7 g-col-md-4 g-start-md-9 g-col-lg-3 g-start-lg-7 g-col-xl-3 g-start-xl-7']/div[@class='price price--medium']/p/text()"
                ).get()
                if price_str:
                    price = price_str.replace('€', '').replace(',', '.').strip()
                    item['price'] = float(price)

                # URL de l'image
                image_url = product.xpath(
                    ".//article/div[@class='product-list__product-area-1 g-col-3 g-col-sm-5 g-col-md-3 g-col-lg-2 g-col-xl-2']/a/@href"
                ).get()
                item['image_url'] = response.urljoin(image_url) if image_url else None

                item['site_name'] = 'Boulanger'
                item['scraped_at'] = datetime.now()

                # Log pour le debugging
                self.logger.info(f"Extracted product: {item['name']} - {item['price']}€")

                yield item

            except Exception as e:
                self.logger.error(f'Error processing product: {str(e)}, Product HTML: {product.get()}')