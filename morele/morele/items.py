# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
import re

def remove_currency(value):
    if value:
        return float(value.replace('zł','').replace(' ','').replace(',','.'))
    return value
        
    
def remove_unit(value):
    if type(value) is int:
        return value
    value = re.sub("\D+", '', value)
    return value    
        

def integer_column_type_get_rid_of_unwanted_string(value):
    if value == 'Brak' or value == 'Nie dotyczy' or value == 'Brak danych':
        return None
    return value
        

def english_replacements(value):
    if value == 'Tak':
        return 'Yes'
    elif value == 'Nie':
        return 'No'
    return value
        

def change_brak_to_zero(value):
    if value == 'Brak':
        return 0
    return value
                   


class MoreleItem(scrapy.Item):
    ean =  scrapy.Field(output_processor = TakeFirst())
    card_length =  scrapy.Field(output_processor = TakeFirst()) 
    dlss_3_0 = scrapy.Field(
        input_processor = MapCompose(english_replacements),
        output_processor = TakeFirst(),
    )
    d_sub = scrapy.Field(
        input_processor = MapCompose(change_brak_to_zero),
        output_processor = TakeFirst(),
    )
    chipset_type = scrapy.Field(output_processor = TakeFirst())
    display_port = scrapy.Field(
        input_processor = MapCompose(change_brak_to_zero),
        output_processor = TakeFirst(),
    )
    mini_display_port = scrapy.Field(
        input_processor = MapCompose(change_brak_to_zero),
        output_processor = TakeFirst(),
    ) 
    dvi = scrapy.Field(
        input_processor = MapCompose(change_brak_to_zero),
        output_processor = TakeFirst(),
    )
    hdmi = scrapy.Field(
        input_processor = MapCompose(change_brak_to_zero),
        output_processor = TakeFirst(),
    )
    usb_c = scrapy.Field(
        input_processor = MapCompose(change_brak_to_zero),
        output_processor = TakeFirst(),
    )
    card_name = scrapy.Field(output_processor = TakeFirst()) 
    card_id = scrapy.Field(output_processor = TakeFirst()) 
    card_price = scrapy.Field(
        input_processor = MapCompose(remove_currency),
        output_processor = TakeFirst(),
    ) 
    stock = scrapy.Field(output_processor = TakeFirst()) 
    rating_count = scrapy.Field(
        input_processor = MapCompose(remove_unit),
        output_processor = TakeFirst(),
    ) 
    questions = scrapy.Field(output_processor = TakeFirst())
    buyers = scrapy.Field(output_processor = TakeFirst()) 
    rating = scrapy.Field(output_processor = TakeFirst()) 
    card_manufacturer = scrapy.Field(output_processor = TakeFirst()) 
    card_manufacturer_code = scrapy.Field(output_processor = TakeFirst())
    chipset_brand = scrapy.Field(output_processor = TakeFirst())   
    clock_speed = scrapy.Field(
        input_processor = MapCompose(remove_unit),
        output_processor = TakeFirst(),
    )
    clock_speed_boost_mode = scrapy.Field(
        input_processor = MapCompose(remove_unit),
        output_processor = TakeFirst(),
    )
    stream_processors = scrapy.Field(
        input_processor = MapCompose(integer_column_type_get_rid_of_unwanted_string),
        output_processor = TakeFirst(),
    )
    rop_units = scrapy.Field(
        input_processor = MapCompose(integer_column_type_get_rid_of_unwanted_string),
        output_processor = TakeFirst(),
    )
    texturing_units = scrapy.Field(
        input_processor = MapCompose(integer_column_type_get_rid_of_unwanted_string),
        output_processor = TakeFirst(),
    )
    rt_cores = scrapy.Field(
        input_processor = MapCompose(integer_column_type_get_rid_of_unwanted_string),
        output_processor = TakeFirst(),
    )
    tensor_cores = scrapy.Field(
        input_processor = MapCompose(integer_column_type_get_rid_of_unwanted_string),
        output_processor = TakeFirst(),
    )
    connector_type = scrapy.Field(output_processor = TakeFirst())
    card_length = scrapy.Field(
        input_processor = MapCompose(remove_unit),
        output_processor = TakeFirst(),
    )
    card_linking = scrapy.Field(
        input_processor = MapCompose(english_replacements),
        output_processor = TakeFirst(),
    )
    card_resolution = scrapy.Field(output_processor = TakeFirst())
    recommended_power_supply_wattage = scrapy.Field(
        input_processor = MapCompose(remove_unit),
        output_processor = TakeFirst(),        
    )
    led_backlighting = scrapy.Field(
        input_processor = MapCompose(english_replacements),
        output_processor = TakeFirst(),
    )
    ram_capacity = scrapy.Field(
        input_processor = MapCompose(remove_unit),
        output_processor = TakeFirst(),
    )
    ram_type = scrapy.Field(output_processor = TakeFirst())
    data_bus = scrapy.Field(output_processor = TakeFirst())
    memory_clock = scrapy.Field(
        input_processor = MapCompose(remove_unit),
        output_processor = TakeFirst(),
    )
    cooling_type = scrapy.Field(output_processor = TakeFirst())
    fans_quantity = scrapy.Field(
        input_processor = MapCompose(integer_column_type_get_rid_of_unwanted_string),
        output_processor = TakeFirst(),
    )
    power_ports = scrapy.Field(output_processor = TakeFirst())
    packaging_version = scrapy.Field(output_processor = TakeFirst())


