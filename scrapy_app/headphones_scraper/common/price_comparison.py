import json
import pandas as pd

def compare_prices(consolidated_data_file):
    """
    Compare les prix des casques entre différents sites
    """
    # Charger les données consolidées
    with open(consolidated_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convertir en DataFrame
    df = pd.DataFrame(data)
    
    # Grouper par modèle et comparer les prix
    price_comparison = df.groupby('model').agg({
        'current_price': ['min', 'max', 'mean'],
        'source_website': list
    }).reset_index()
    
    # Renommer les colonnes
    price_comparison.columns = ['Model', 'Min Price', 'Max Price', 'Average Price', 'Sources']
    
    # Sauvegarder le rapport de comparaison
    report_filename = 'price_comparison_report.csv'
    price_comparison.to_csv(report_filename, index=False)
    
    print(f"Rapport de comparaison sauvegardé dans {report_filename}")
    return price_comparison

if __name__ == '__main__':
    # Utiliser le dernier fichier consolidé
    import glob
    import os
    
    data_files = glob.glob('scraped_data/consolidated_headphones_*.json')
    latest_file = max(data_files, key=os.path.getctime)
    
    compare_prices(latest_file)
