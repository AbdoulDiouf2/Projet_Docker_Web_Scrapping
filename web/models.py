import mysql.connector
from config import Config

class Database:
    def __init__(self):
        self.config = Config.MYSQL_CONFIG

    def get_connection(self):
        return mysql.connector.connect(**self.config)

    def get_all_products(self):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                WITH price_info AS (
                    SELECT name, MIN(price) as min_price
                    FROM products
                    GROUP BY name
                )
                SELECT 
                    p.*,
                    pi.min_price,
                    p.price = pi.min_price as is_cheapest
                FROM products p
                JOIN price_info pi ON p.name = pi.name
                ORDER BY p.price ASC
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def search_products(self, search_term):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                WITH ranked_products AS (
                    SELECT 
                        *,
                        ROW_NUMBER() OVER (PARTITION BY site_name ORDER BY price ASC) as price_rank
                    FROM products
                    WHERE name LIKE %s
                )
                SELECT * FROM ranked_products
                WHERE price_rank <= 30
                ORDER BY site_name, price_rank
            """
            cursor.execute(query, (f'%{search_term}%',))
            all_products = cursor.fetchall()
            
            # Organiser les résultats par site
            results = {
                'Boulanger': [],
                'CDiscount': [],
                'eBay': []
            }
            
            for product in all_products:
                if len(results[product['site_name']]) < 30:
                    results[product['site_name']].append(product)
            
            return results
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def get_product_by_id(self, product_id):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT * FROM products
                WHERE id = %s
            """
            cursor.execute(query, (product_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_products_by_site(self, site_name):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = """
                SELECT * FROM products
                WHERE site_name = %s
            """
            cursor.execute(query, (site_name,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()