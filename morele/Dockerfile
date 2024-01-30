FROM python:3.11.6

WORKDIR /morele_webscraping

COPY . . 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["scrapy", "crawl", "morele_spider"]