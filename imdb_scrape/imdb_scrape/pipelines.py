# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter

def format_number(num):
    if num is None:
        return None
    return "{:,.2f}".format(num)

class ImdbScrapePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Convert runtime to hours
        run_time = adapter.get('run_time')
        if run_time:
            adapter['run_time'] = self.convert_runtime_to_hours(run_time)
        
        # Convert rating to float
        rating = adapter.get('rating')
        if rating:
            adapter['rating'] = float(rating)
        
        # Convert num_reviews to integer
        num_reviews = adapter.get('num_reviews')
        if num_reviews:
            adapter['num_reviews'] = self.convert_reviews_to_int(num_reviews)
        
        # Convert budget, gross_na, gross_globe to float
        budget = adapter.get('budget')
        if budget:
            adapter['budget'] = self.convert_currency_to_float(budget)
        
        gross_na = adapter.get('gross_na')
        if gross_na:
            adapter['gross_na'] = self.convert_currency_to_float(gross_na)
        
        gross_globe = adapter.get('gross_globe')
        if gross_globe:
            adapter['gross_globe'] = self.convert_currency_to_float(gross_globe)
        
        # Convert year to integer
        year = adapter.get('year')
        if year:
            adapter['year'] = int(year)

        return item

    def convert_runtime_to_hours(self, runtime_str):
        match = re.match(r'(?:(\d+)h )?(?:(\d+)m)?', runtime_str)
        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            total_hours = hours + (minutes / 60)
            formatted_total_hours = "{:,.2f}".format(total_hours)
            return formatted_total_hours
        return None

    def convert_reviews_to_int(self, reviews_str):
        reviews_str = reviews_str.upper().replace('K', 'e3').replace('M', 'e6').replace(',', '')
        try:
            return int(float(reviews_str))
        except ValueError:
            return None

    def convert_currency_to_float(self, currency_str):
        if currency_str:
            currency_str = currency_str.replace('$', '').replace(',', '')
            try:
                currency_float = float(currency_str)
                return format_number(currency_float)
            except ValueError:
                return None
        return None
    

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

class SaveToMySQLPipeline:

    def __init__(self):
        # Connect to MySQL using environment variables
        self.conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )

        # Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        # Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title TEXT,
            year INT,
            parent_guide VARCHAR(255),
            run_time FLOAT,
            rating FLOAT,
            num_reviews INTEGER,
            popularity VARCHAR(255),
            genre VARCHAR(255),
            director VARCHAR(255),
            writer TEXT,
            stars TEXT,
            budget FLOAT,
            gross_na FLOAT,
            gross_globe FLOAT,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        # Convert list fields to comma-separated strings
        item['writer'] = ', '.join(item['writer']) if item['writer'] else None
        item['stars'] = ', '.join(item['stars']) if item['stars'] else None

        # Define insert statement
        self.cur.execute(""" 
        INSERT INTO books (
            url, 
            title, 
            year, 
            parent_guide, 
            run_time,
            rating,
            num_reviews,
            popularity,
            genre,
            director,
            writer,
            stars,
            budget,
            gross_na,
            gross_globe
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )""", (
            item.get("url"),
            item.get("title"),
            item.get("year"),
            item.get("parent_guide"),
            item.get("run_time"),
            item.get("rating"),
            item.get("num_reviews"),
            item.get("popularity"),
            item.get("genre"),
            item.get("director"),
            item.get("writer"),
            item.get("stars"),
            item.get("budget"),
            item.get("gross_na"),
            item.get("gross_globe")
        ))

        # Execute insert of data into database
        self.conn.commit()

        return item

    def close_spider(self, spider):
        # Close cursor & connection to database 
        self.cur.close()
        self.conn.close()