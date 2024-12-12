import mysql.connector
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class MySQLPipeline:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.stats = {
            'inserted': 0,
            'updated': 0,
            'errors': 0
        }

    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host=spider.settings.get('MYSQL_CONFIG')['host'],
                user=spider.settings.get('MYSQL_CONFIG')['user'],
                password=spider.settings.get('MYSQL_CONFIG')['password'],
                database=spider.settings.get('MYSQL_CONFIG')['database']
            )
            self.cur = self.conn.cursor()
            spider.logger.info("Successfully connected to MySQL database")
        except Exception as e:
            spider.logger.error(f"Error connecting to MySQL database: {e}")
            raise

    def close_spider(self, spider):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.commit()
                self.conn.close()
            spider.logger.info(f"""Scraping finished. Statistics:
                - New products inserted: {self.stats['inserted']}
                - Products updated: {self.stats['updated']}
                - Errors: {self.stats['errors']}""")
        except Exception as e:
            spider.logger.error(f"Error during pipeline closure: {e}")

    def process_item(self, item, spider):
        try:
            # Vérification des données requises
            if not item.get('name') or not item.get('price') or not item.get('product_url'):
                raise DropItem(f"Missing required fields in {item}")

            # Vérifie si le produit existe déjà
            check_sql = "SELECT id, price FROM products WHERE product_url = %s"
            self.cur.execute(check_sql, (item['product_url'],))
            existing_product = self.cur.fetchone()

            if existing_product:
                # Mise à jour du produit existant
                old_price = existing_product[1]
                update_sql = """
                UPDATE products 
                SET name = %s, 
                    price = %s, 
                    site_name = %s, 
                    image_url = %s, 
                    scraped_at = %s
                WHERE product_url = %s
                """
                self.cur.execute(update_sql, (
                    item['name'],
                    item['price'],
                    item['site_name'],
                    item['image_url'],
                    item['scraped_at'],
                    item['product_url']
                ))
                self.stats['updated'] += 1
                
                if old_price != item['price']:
                    spider.logger.info(f"Price updated for {item['name']}: {old_price} -> {item['price']}")
            else:
                # Insertion d'un nouveau produit
                insert_sql = """
                INSERT INTO products 
                (name, price, site_name, product_url, image_url, scraped_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                self.cur.execute(insert_sql, (
                    item['name'],
                    item['price'],
                    item['site_name'],
                    item['product_url'],
                    item['image_url'],
                    item['scraped_at']
                ))
                self.stats['inserted'] += 1
                spider.logger.info(f"New product inserted: {item['name']}")
            
            self.conn.commit()
            return item

        except Exception as e:
            self.stats['errors'] += 1
            spider.logger.error(f"Error processing item {item.get('name', 'Unknown')}: {e}")
            raise DropItem(f"Failed to save item: {e}")