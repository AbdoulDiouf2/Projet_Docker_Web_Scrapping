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
- **Flask/FastAPI**: Serveur web (à définir)
- **PHPMyAdmin**: Interface d'administration de la base de données

## 📁 Structure du Projet

```
projet/
├── docker-compose.yml
├── README.md
├── scrapy_app/          # Application de scraping
├── web_app/            # Application web
└── mysql/             # Configuration MySQL
```
## 📁 Structure du Projet
├── docker-compose.yml
├── README.md
├── scrapy_app/
│   ├── Dockerfile
│   └── price_comparator/
│       ├── spiders/
│       ├── items.py
│       ├── pipelines.py
│       └── settings.py
├── web_app/
│   ├── Dockerfile
│   ├── static/
│   ├── templates/
│   └── app.py
└── mysql/
    ├── Dockerfile
    └── init.sql

## 🚦 Prérequis

- Docker
- Docker Compose

## 🔧 Installation

1. Cloner le repository
2. Lancer les conteneurs avec Docker Compose :
   ```bash
   docker-compose up
   ```

## 👥 Équipe

- [Membre 1]
- [Membre 2]
- [Membre 3]

## 📝 License

Ce projet est réalisé dans le cadre d'un projet scolaire à l'ESIGELEC.


