import scrapy

class HeadphoneItem(scrapy.Item):
    source_website = scrapy.Field()
    scrape_timestamp = scrapy.Field()
    
    brand = scrapy.Field()
    model = scrapy.Field()
    full_name = scrapy.Field()
    
    current_price = scrapy.Field()
    original_price = scrapy.Field()
    discount_percentage = scrapy.Field()
    currency = scrapy.Field()
    
    type = scrapy.Field()
    connection_type = scrapy.Field()
    noise_cancellation = scrapy.Field()
    battery_life = scrapy.Field()
    color = scrapy.Field()
    
    in_stock = scrapy.Field()
    delivery_options = scrapy.Field()
    
    product_url = scrapy.Field()
    product_image_url = scrapy.Field()
