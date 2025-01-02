from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from price_scraper.spiders.boulanger_spider import BoulangerSpider
from price_scraper.spiders.cdiscount_spider import CdiscountSpider

def test_spider():
    settings = get_project_settings()
    
    # Ajouter le pipeline de test
    settings.set('ITEM_PIPELINES', {'price_scraper.pipelines.MySQLPipeline': 300})
    
    process = CrawlerProcess(settings)
    process.crawl(CdiscountSpider)
    process.crawl(BoulangerSpider)
    process.start()

if __name__ == '__main__':
    test_spider()