import scrapy
from datetime import datetime
from ..items import ProductItem

class BoulangerSpider(scrapy.Spider):
    name = 'boulanger'
    
    def start_requests(self):
        # On commence par la première page
        url = 'https://www.boulanger.com/c/nav-filtre/resultats?tr=casque&brand~apple|brand~asus|brand~beats|brand~bose|brand~jabra|brand~jbl|brand~jvc|brand~philips|brand~samsung'
        yield scrapy.Request(url, callback=self.parse, meta={'page': 1})
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    def parse(self, response):
        current_page = response.meta['page']
        self.logger.info(f'Scraping page {current_page}')
        
        products = response.xpath("//ul/li[@class=' product-list__item']")
        products_count = len(products)
        self.logger.info(f'Found {products_count} products on page {current_page}')

        # Si aucun produit trouvé, on arrête
        if products_count == 0:
            self.logger.info('No more products found, stopping.')
            return

        for product in products:
            try:
                item = ProductItem()
                
                # Nom du produit
                name_parts = []
                pre_strong = product.xpath(".//h2/text()").getall()
                strong_text = product.xpath(".//h2/strong/text()").get()
                
                if pre_strong:
                    name_parts.extend([part.strip() for part in pre_strong if part.strip()])
                if strong_text:
                    name_parts.append(strong_text.strip())
                
                item['name'] = " ".join(name_parts).strip()
                
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
                srcset = product.xpath(
                    ".//article/div[@class='product-list__product-area-1 g-col-3 g-col-sm-5 g-col-md-3 g-col-lg-2 g-col-xl-2']/a/picture/img/@srcset"
                ).get()
                
                if srcset:
                    image_url = srcset.split(' ')[0]
                    item['image_url'] = image_url
                else:
                    image_url = product.xpath(
                        ".//article/div[@class='product-list__product-area-1 g-col-3 g-col-sm-5 g-col-md-3 g-col-lg-2 g-col-xl-2']/a/picture/img/@src"
                    ).get()
                    item['image_url'] = image_url

                item['site_name'] = 'Boulanger'
                item['scraped_at'] = datetime.now()

                yield item

            except Exception as e:
                self.logger.error(f'Error processing product: {str(e)}')

        # Si on a trouvé des produits, on passe à la page suivante
        if products_count > 0:
            next_page = current_page + 1
            next_url = f'https://www.boulanger.com/c/nav-filtre/resultats?tr=casque&brand~apple|brand~asus|brand~beats|brand~bose|brand~jabra|brand~jbl|brand~jvc|brand~philips|brand~samsung&numPage={next_page}'
            self.logger.info(f'Going to next page: {next_url}')
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={'page': next_page}
            )