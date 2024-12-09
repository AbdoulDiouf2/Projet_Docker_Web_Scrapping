# Scraper de Casques Multi-Sites

## 🚀 Installation

1. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```
 
2. Installer les dépendances
```bash
pip install -r requirements.txt
```

## 🕷️ Lancer les Scrapers

```bash
# Scraper Boulanger
scrapy crawl boulanger

# Scraper Fnac
scrapy crawl fnac

# Scraper Darty
scrapy crawl darty
```

## 📦 Données Scrapées

Les données sont sauvegardées dans :
- `scraped_data/boulanger_headphones_YYYYMMDD.json`
- `scraped_data/fnac_headphones_YYYYMMDD.json`
- `scraped_data/darty_headphones_YYYYMMDD.json`

## 🔍 Structure des Données

- `source_website`: Source du scraping
- `brand`: Marque du casque
- `model`: Modèle du casque
- `current_price`: Prix actuel
- `product_url`: Lien vers le produit

## 🔍 Scripts Additionnels

### Consolidation des Données
```bash
python -m headphones_scraper.common.consolidate_data
```

### Comparaison de Prix
```bash
python -m headphones_scraper.common.price_comparison
```

## 🤝 Workflow Collaboratif

1. Travaillez sur votre branche personnelle
2. Respectez le format de données commun
3. Faites des Pull Requests pour les revues de code
