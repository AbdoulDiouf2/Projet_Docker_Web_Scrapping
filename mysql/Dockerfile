FROM mysql:8.0

# Variables d'environnement pour la configuration initiale
ENV MYSQL_DATABASE=comparateur_prix
ENV MYSQL_USER=hadoop
ENV MYSQL_PASSWORD=team_hadoop
ENV MYSQL_ROOT_PASSWORD=team_hadoop

# Copie du script d'initialisation
COPY init.sql /docker-entrypoint-initdb.d/

# Configuration du jeu de caractères
CMD ["mysqld", "--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]