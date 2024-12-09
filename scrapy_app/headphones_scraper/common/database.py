import mysql.connector
import json
import os

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
    
    def insert_headphones(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Requête d'insertion à adapter selon votre schéma
        query = """
        INSERT INTO headphones 
        (source_website, brand, model, full_name, current_price, product_url) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        values = (
            data['source_website'],
            data['brand'],
            data['model'],
            data['full_name'],
            data['current_price'],
            data['product_url']
        )
        
        self.cursor.execute(query, values)
        self.connection.commit()
    
    def close(self):
        self.cursor.close()
        self.connection.close()
