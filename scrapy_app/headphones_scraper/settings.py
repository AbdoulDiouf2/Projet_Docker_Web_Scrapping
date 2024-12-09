BOT_NAME = 'headphones_scraper'

SPIDER_MODULES = ['headphones_scraper.spiders']
NEWSPIDER_MODULE = 'headphones_scraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16

# Configure item pipelines
ITEM_PIPELINES = {
   'headphones_scraper.pipelines.HeadphoneScraperPipeline': 300,
}

# Logging configuration
LOG_LEVEL = 'INFO'
