class Config:
    MYSQL_CONFIG = {
        'host': 'db',
        'user': 'hadoop',
        'password': 'team_hadoop',
        'database': 'comparateur_prix'
    }
    DEBUG = True
    SECRET_KEY = 'your-secret-key-here'  # Pour la sécurité de Flask