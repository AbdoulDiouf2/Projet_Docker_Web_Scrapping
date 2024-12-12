import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    site_name = scrapy.Field()
    product_url = scrapy.Field()
    image_url = scrapy.Field()
    description = scrapy.Field()
    scraped_at = scrapy.Field()