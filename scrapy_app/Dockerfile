FROM python:3.11

WORKDIR /app

# Copier les fichiers du projet
COPY requirements.txt .
COPY price_scraper/ ./price_scraper/
COPY test_spider.py .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut
CMD ["python", "test_spider.py"]