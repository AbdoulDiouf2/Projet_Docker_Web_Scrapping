import json
from datetime import datetime
import os

class HeadphoneScraperPipeline:
    def open_spider(self, spider):
        # Créer un dossier pour stocker les données si non existant
        os.makedirs('scraped_data', exist_ok=True)
        
    def close_spider(self, spider):
        # Optionnel : actions à la fin du scraping
        pass
    
    def process_item(self, item, spider):
        # Convertir l'item en dictionnaire
        item_dict = dict(item)
        
        # Ajouter un timestamp si non présent
        if 'scrape_timestamp' not in item_dict:
            item_dict['scrape_timestamp'] = datetime.now().isoformat()
        
        # Chemin de sauvegarde
        filename = f"scraped_data/{spider.name}_headphones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Sauvegarder en JSON
        with open(filename, 'a', encoding='utf-8') as f:
            json.dump(item_dict, f, ensure_ascii=False, indent=2)
            f.write('\n')
        
        return item
