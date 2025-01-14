FROM mysql:8.0

# Variables d'environnement pour la configuration initiale
# Importation des variables d'environnement depuis le fichier .env
ENV MYSQL_DATABASE=${MYSQL_DATABASE}
ENV MYSQL_USER=${MYSQL_USER}
ENV MYSQL_PASSWORD=${MYSQL_PASSWORD}
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

# Copie du script d'initialisation
COPY init.sql /docker-entrypoint-initdb.d/

# Configuration du jeu de caractères
CMD ["mysqld", "--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]