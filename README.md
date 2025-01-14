# Comparateur de Prix - Projet Docker & Web Scraping

Ce projet est un comparateur de prix qui collecte des informations sur les produits de différents sites e-commerce et permet de comparer leurs prix.

## 🚀 Fonctionnalités

- Scraping de données produits depuis plusieurs sites e-commerce
- Stockage des données dans une base MySQL
- Interface web pour visualiser et comparer les prix
- Liens directs vers les pages produits
- Mise en évidence des meilleures offres

## 🛠️ Technologies Utilisées

- **Scrapy**: Pour le web scraping
- **MySQL**: Base de données
- **Docker**: Conteneurisation
- **Docker Compose**: Orchestration des conteneurs
- **Flask**: Serveur web
- **PHPMyAdmin**: Interface d'administration de la base de données

## 📁 Structure du Projet

```
projet/
├── docker-compose.yml
├── README.md
├── .env
├── scrapy_app/          # Application de scraping
│   ├── Dockerfile
│   ├── price_scraper/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   ├── pipelines.py
│   │   ├── settings.py
│   │   └── spiders/
│   │       ├── __init__.py
│   │       ├── boulanger_spider.py
│   │       ├── cdiscount_spider.py
│   │       └── ebay_spider.py
│   ├── README.md
│   ├── requirements.txt
│   ├── scrapy.cfg
│   └── test_spider.py
├── web/                # Application web
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── models.py
│   ├── requirements.txt
│   └── templates/
│       ├── base.html
│       └── index.html
└── mysql/              # Configuration MySQL
    ├── Dockerfile
    └── init.sql
```

## 🚦 Prérequis

- Docker
- Docker Compose

## 🔧 Installation et Démarrage

1. Cloner le repository
2. Créer un fichier `.env` à la racine du projet avec le contenu suivant :
   ```properties
   MYSQL_ROOT_PASSWORD=your_root_password
   MYSQL_DATABASE=comparateur_prix
   MYSQL_USER=your_database_user
   MYSQL_PASSWORD=your_database_password
   ```
3. Lancer les conteneurs avec Docker Compose :
   ```bash
   docker-compose up
   ```

## 🌐 Accès aux Services

- **Application Web**: http://localhost:5000
- **PHPMyAdmin**: http://localhost:8080

## 👥 Équipe

- AMAR Cheikh Mbacké
- DIOUF Abdoul Ahad Mbacké
- SOW Aminata
