-- Création de la base de données
CREATE DATABASE IF NOT EXISTS comparateur_prix CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE comparateur_prix;

-- Table unique pour les produits
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    site_name VARCHAR(50) NOT NULL,  -- 'Boulanger', 'Fnac', ou 'Darty'
    product_url VARCHAR(500) NOT NULL,
    image_url VARCHAR(500),
    description TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Création d'un index pour accélérer les recherches par site
CREATE INDEX idx_site_name ON products(site_name);