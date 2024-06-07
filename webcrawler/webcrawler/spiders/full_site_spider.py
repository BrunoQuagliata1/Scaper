import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pymongo import MongoClient
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging

class FullSiteSpider(CrawlSpider):
    name = "full_site_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super(FullSiteSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]
        self.client = MongoClient('mongodb+srv://brunoquagliata:qyNcpbRjYSi3AyQO@scraper.udhztee.mongodb.net/')
        self.db = self.client['webData2']
        self.collection = self.db['pages']
        logging.info(f"Starting crawl for: {start_url}")

    rules = (
        Rule(LinkExtractor(allow=(), deny=()), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        logging.info(f"Crawling URL: {response.url}")
        #Extract data from the response
        soup = BeautifulSoup(response.body, 'html.parser')

        #  Define tags to exclude
        [s.extract() for s in soup(['nav', 'footer', 'header', 'script', 'style', 'aside'])]

        # Extractr the main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        if main_content:
            text_content = main_content.get_text(separator='\n', strip=True)
        else:
            text_content = soup.get_text(separator='\n', strip=True)

        self.collection.insert_one({
            'url': response.url,
            'content': text_content,
            'date': response.headers.get('Date').decode('utf-8')
        })

    def closed(self, reason):
        logging.info("Crawl finished")
        self.client.close()
