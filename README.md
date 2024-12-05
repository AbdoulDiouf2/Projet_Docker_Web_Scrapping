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

## 🚦 Prérequis

- Docker
- Docker Compose

## 🔧 Installation et Démarrage

1. Cloner le repository
2. Lancer les conteneurs avec Docker Compose :
   ```bash
   docker-compose up
   ```

## 🌐 Accès aux Services

- **Application Web**: http://localhost:5000
- **PHPMyAdmin**: http://localhost:8080
  - Utilisateur: ...
  - Mot de passe: ...
- **MySQL**:
  - Port: 3306
  - Base de données: price_comparison
  - Utilisateur: ...
  - Mot de passe: ...

## 👥 Équipe

- AMAR Cheikh Mbacké
- DIOUF Abdoul Ahad Mbacké
- SOW Aminata