import json
import os
from datetime import datetime

def consolidate_scraped_data(data_dir='scraped_data'):
    """
    Consolide les données de scraping de tous les sites
    """
    consolidated_data = []
    
    # Parcourir tous les fichiers JSON dans le dossier
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(data_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                consolidated_data.append(data)
    
    # Nom du fichier de consolidation
    output_filename = f'consolidated_headphones_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    output_path = os.path.join(data_dir, output_filename)
    
    # Sauvegarder les données consolidées
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(consolidated_data, f, ensure_ascii=False, indent=2)
    
    print(f"Données consolidées sauvegardées dans {output_path}")
    return output_path

if __name__ == '__main__':
    consolidate_scraped_data()
