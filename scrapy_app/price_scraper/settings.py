BOT_NAME = 'price_scraper'

SPIDER_MODULES = ['price_scraper.spiders']
NEWSPIDER_MODULE = 'price_scraper.spiders'

# Respecter les règles robots.txt
ROBOTSTXT_OBEY = True

# Configure item pipelines
# Commentons temporairement le pipeline MySQL pour le test
# ITEM_PIPELINES = {
#    'price_scraper.pipelines.MySQLPipeline': 300,
# }

# Configuration des délais entre les requêtes
DOWNLOAD_DELAY = 2

# Headers par défaut
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'fr',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}