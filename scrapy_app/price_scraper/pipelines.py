import json
from datetime import datetime

class TestPipeline:
    def open_spider(self, spider):
        self.file = open('boulanger_products.json', 'w', encoding='utf-8')
        self.items = []

    def close_spider(self, spider):
        # Formatage des données pour une meilleure lisibilité
        for item in self.items:
            if 'scraped_at' in item:
                item['scraped_at'] = item['scraped_at'].strftime('%Y-%m-%d %H:%M:%S')
        
        json.dump(self.items, self.file, ensure_ascii=False, indent=2)
        self.file.close()

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item