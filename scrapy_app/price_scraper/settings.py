BOT_NAME = 'price_scraper'

SPIDER_MODULES = ['price_scraper.spiders']
NEWSPIDER_MODULE = 'price_scraper.spiders'

ROBOTSTXT_OBEY = False

# Configuration des délais entre les requêtes
DOWNLOAD_DELAY = 2

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'fr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Activer le pipeline MySQL
ITEM_PIPELINES = {
   'price_scraper.pipelines.MySQLPipeline': 300,
}

# Configuration MySQL
MYSQL_CONFIG = {
    'host': 'db',  # nous modifierons ceci pour l'adapter à Docker
    'user': 'hadoop',
    'password': 'team_hadoop',
    'database': 'comparateur_prix'
}