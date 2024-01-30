# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import logging
import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)  




class MorelePipeline:
    def process_item(self, item, spider):
        return item


class SavingToSQLPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):        
        self.connection = psycopg2.connect(     
        user = os.environ['POSTGRES_USER'],
        database = os.environ['POSTGRES_DB'],
        password = os.environ['POSTGRES_PASSWORD'],    
        host='postgres',
        port='5432')

        self.curr = self.connection.cursor()

    def process_item(self,item,spider):
        self.upload_db(item)
        return item

    def upload_db(self,item):
        vals = [item[x] for x in item]
        vals_str_list = ["%s"] * len(vals)
        vals_str = ", ".join(vals_str_list)         
        self.curr.execute("INSERT INTO graphic_cards ({cols}) VALUES ({vals_str})".format(
        cols = str(list(item.keys()))[1:-1].replace("'",""), vals_str = vals_str), vals)
        self.connection.commit()

        
        
        