class Config:
    MYSQL_CONFIG = {
        'host': 'db',
        'user': 'hadoop',
        'password': 'team_hadoop',
        'database': 'comparateur_prix'
    }
    DEBUG = False  # Set to False in production
    # SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable for secret key