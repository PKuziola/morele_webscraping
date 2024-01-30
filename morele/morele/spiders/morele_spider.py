import scrapy
from bs4 import BeautifulSoup
import logging
import re
from ..items import MoreleItem
import psycopg2
from scrapy.loader import ItemLoader


class MoreleSpiderSpider(scrapy.Spider):
    name = "morele_spider"
    start_urls = ["https://www.morele.net/kategoria/karty-graficzne-12/"]
    url_link = 'https://www.morele.net/kategoria/karty-graficzne-12/,,,,,,,,0,,,,'
    page = 1
    

    def parse(self, response):
        for product in response.css("a.productLink"):
            link = product.css("a.productLink").attrib["href"]
            url = f"https://www.morele.net{link}"
            yield scrapy.Request(url=url, callback=self.parse_ad_page)

        self.page += 1
        next_page = f"{self.url_link}/{self.page}/"
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_ad_page(self, response):
        loader = ItemLoader(item=MoreleItem())
        doc = BeautifulSoup(response.text, "html.parser")        

        item = {
            'ean': None,
            'dlss_3_0': None,
            'd_sub': None,
            'display_port': None,
            'mini_display_port': None,
            'dvi': None,
            'hdmi': None,
            'usb_c': None,
            'card_name': None,
            'card_id': None,
            'card_price': None,
            'stock': 0,
            'rating_count': 0,
            'questions': 0,
            'buyers': 0,
            'rating': None,
            'card_manufacturer': None,
            'card_manufacturer_code': None,
            'chipset_brand': None,
            'chipset_type': None,
            'clock_speed': None,
            'clock_speed_boost_mode': None,
            'stream_processors': None,
            'rop_units': None,
            'texturing_units': None,
            'rt_cores': None,
            'tensor_cores': None,
            'connector_type': None,
            'card_length': None,
            'card_linking': None,
            'card_resolution': None,
            'recommended_power_supply_wattage': None,
            'led_backlighting': None,
            'ram_capacity': None,
            'ram_type': None,
            'data_bus': None,
            'memory_clock': None,
            'cooling_type': None,
            'fans_quantity': None,
            'power_ports': None, 
            'packaging_version': None
        }

        item = self.get_general_specs(doc, response, item)
        item = self.get_detailed_specs(doc, response, item)

        for key, value in item.items():
            loader.add_value(f"{key}", value)
        yield loader.load_item()


    def get_general_specs(self, doc, response, item):
        """
        Function is reponsible for webscraping basic parameters which are located on the top of the page and updating the dictionary with new values

        Args:
            doc: BeautifulSoup object
            response: HTTP response object
            item: Dictionary with variables representing parameters that we want to obtain from webpage

        Returns:
            Dictionary with updated values where necessary
        """
        card_name = response.css("h1.prod-name::text").get()
        card_id = response.css("div.grey-action > span::text").get()
        card_price = response.css("div.product-price").attrib.get("data-default")        

        item.update(
            {
                "card_name": card_name,
                "card_id": card_id,
                "card_price": card_price    
            }
        )

        stock_string = response.css("div.prod-available-items::text").get()
        stock_match = re.search(r"\d+", stock_string)
        item.update({"stock": int(stock_match.group()) if stock_match else 0})

        question_string = doc.find("div", {"class": "prod-tech has-questions"})
        if question_string is not None:
            question_string = doc.find("div", {"class": "prod-tech has-questions"}).text
            if re.search("[0-9]+ pyta", question_string) is not None:
                latter_search = re.search("[0-9]+ pyta", question_string).group(0)
                questions = re.search("[0-9]+", latter_search).group(0)
                item.update({"questions": questions})

        buyers_string = doc.find(
            "div", {"class": "prod-sold btn-get-sold-info text-link-2"}
        )
        if buyers_string is not None:
            buyers_string = doc.find(
                "div", {"class": "prod-sold btn-get-sold-info text-link-2"}
            ).text
            if re.search("[0-9]+", buyers_string) is not None:
                buyers = re.search("[0-9]+", buyers_string).group(0)
                item.update({"buyers": buyers})

        stars_box_selector = "div.prod-info-inside>div.prod-stars-sold-fb>div.prod-stars>div.stars-box"

        if response.css(stars_box_selector).get() is not None:
            rating_count_selector = f"{stars_box_selector} > span.rating-count::text"
            rating_count = response.css(rating_count_selector).get()
            rating_count = re.search(r"\d+", rating_count).group(0) if rating_count else None

            item.update({"rating_count": rating_count})

            stars_box = response.css(stars_box_selector).get()

            checked_value_search = re.search(r'value=["]([0-9]{1}\.[0-9]{2}).+checked', stars_box)
    
            if checked_value_search is not None:
                rating = checked_value_search.group(1)
                item.update({"rating": rating})

        return item
    

    def get_detailed_specs(self, doc, response, item):
        """
        Function is reponsible for webscraping all parameters available under 'Specyfikacja' label at the bottom of the page and updating the dictionary with new values

        Args:
            doc: BeautifulSoup object
            response: HTTP response object
            item: Dictionary with variables representing parameters that we want to obtain from webpage

        Returns:
            Dictionary with updated values where necessary
        """

        variables_mapping_dict = {
            "Producent": "card_manufacturer",
            "EAN": "ean",
            "MiniDisplayPort": "mini_display_port",
            "DVI": "dvi",
            "HDMI": "hdmi",
            "DLSS 3.0": "dlss_3_0",
            "DisplayPort": "display_port",
            'D-Sub': 'd_sub',
            "USB-C": "usb_c",
            "Kod producenta": "card_manufacturer_code",
            'Producent chipsetu': 'chipset_brand',
            'Rodzaj chipsetu': 'chipset_type',
            'Taktowanie rdzenia': 'clock_speed',
            'Taktowanie rdzenia w trybie boost': 'clock_speed_boost_mode',
            'Procesory strumieniowe': 'stream_processors',
            'Jednostki ROP': 'rop_units',
            'Jednostki teksturujące': 'texturing_units',
            'Rdzenie RT': 'rt_cores',
            'Rdzenie Tensor': 'tensor_cores',
            'Typ złącza': 'connector_type',
            'Długość karty': 'card_length',
            'Łączenie kart': 'card_linking',
            'Rozdzielczość': 'card_resolution',
            'Rekomendowana moc zasilacza': 'recommended_power_supply_wattage',
            'Podświetlenie LED': 'led_backlighting',
            'Ilość pamięci RAM': 'ram_capacity',
            'Rodzaj pamięci RAM': 'ram_type',
            'Szyna danych': 'data_bus',
            'Taktowanie pamięci': 'memory_clock',
            'Typ chłodzenia': 'cooling_type',
            'Ilość wentylatorów': 'fans_quantity',
            'Złącza zasilania': 'power_ports',
            'Wersja opakowania': 'packaging_version'
        }

        specification_section = ("div.product-specification__table > div.product-specification__group > div.group__specification > div.specification__row")
        specification_section_base = response.css(specification_section) 

        response_css_specification_row = response.css(specification_section).getall()
        response_css_specification_name = specification_section_base.css("span.specification__name").getall()
        response_css_specification_name_text = specification_section_base.css("span.specification__name ::text").getall()
        response_css_specification_values_text = specification_section_base.css("span.specification__value ::text").getall()
   
       
        temp_list = []
        for element in response_css_specification_values_text:
            element = element.replace("\n", "")
            temp_list.append(element)

        temp_list_filtered = list(filter(lambda x: x != "", temp_list))

        temp_list_2 = []
        temp_list_3 = []
        for element in response_css_specification_name_text:
            element = element.replace("\n", "")
            temp_list_2.append(element)
        if "" in temp_list_2:
            temp_list_2.remove("")
        else:
            pass

        for element in response_css_specification_name:
            if re.search(">.+</span>", element) is not None:
                questionss = re.search(">.+</span>", element).group(0)
                questionss = questionss[1:-7]
            else:
                questionss = re.search("\n.+<i", element).group(0)
                questionss = (
                    re.search(r"^\s*(.*?)(?=<i|$)", questionss, flags=re.UNICODE)
                    .group(0)
                    .strip()
                )
            temp_list_3.append(questionss)

        values_final = temp_list_filtered

        keys_temp = []
        values_temp = []
        if len(temp_list_3) == 33 and len(values_final) == 32:
            for element in response_css_specification_row:
                if (
                    re.search('class="specification__name">.+</span>', element)
                    is not None
                ):
                    latter_search = re.search(
                        'class="specification__name">.+</span>', element
                    ).group(0)
                    key_value = re.search(">.+<", latter_search).group(0)[1:-1]
                elif (
                    re.search('class="specification__name">\n<span>.+</span>', element)
                    is not None
                ):
                    latter_search = re.search(
                        'class="specification__name">\n<span>.+</span>', element
                    ).group(0)
                    key_value = re.search("<span>.+</span>", latter_search).group(0)[
                        6:-7
                    ]
                elif re.search('data-id="[0-9]+">\n.+<i class', element) is not None:
                    latter_search = re.search(
                        'data-id="[0-9]+">\n.+<i class', element
                    ).group(0)
                    key_value = re.search(".+<i class", latter_search).group(0)[:-8]
                else:
                    key_value = None
                keys_temp.append(key_value)
                if re.search(r'itemprop=".+">.+</span>', element) is not None:
                    latter_search = re.search(
                        r'itemprop=".+">.+</span>', element
                    ).group(0)
                    value_value = re.search(r">.+<", latter_search).group(0)[1:-1]
                elif (
                    re.search(r'class="specification__value">.+</span>', element)
                    is not None
                ):
                    latter_search = re.search(
                        r'class="specification__value">.+</span>', element
                    ).group(0)
                    value_value = re.search(r">.+<", latter_search).group(0)[1:-1]
                elif re.search(r'itemprop=".+">\n.+\n<', element) is not None:
                    latter_search = re.search(r'itemprop=".+">\n.+\n<', element).group(
                        0
                    )
                    value_value = re.search(r"\n.+\n", latter_search).group(0).strip()
                elif (
                    re.search(
                        r'class="specification__item">\n<span>.+<span class', element
                    )
                    is not None
                ):
                    latter_search = re.search(
                        r'class="specification__item">\n<span>.+<span class', element
                    ).group(0)
                    value_value = re.search(r">.+<", latter_search).group(0)[1:-1]
                elif re.search(r'data-id=".+">\n.+<span class', element) is not None:
                    latter_search = re.search(
                        r'data-id=".+">\n.+<span class', element
                    ).group(0)
                    value_value = (
                        re.search(r"\n.+<", latter_search).group(0).strip()[:-1]
                    )
                else:
                    value_value = None
                values_temp.append(value_value)
            temp_item = {keys_temp[i]: values_temp[i] for i in range(len(values_temp))}
        else:
            temp_item = {temp_list_3[i]: values_final[i] for i in range(len(values_final))}       

        keys_to_update = list(temp_item.keys())
        for key in keys_to_update:
            if key in variables_mapping_dict.keys():
                temp_item[variables_mapping_dict[key]] = temp_item.pop(key)        

        item.update(temp_item) 

        return item