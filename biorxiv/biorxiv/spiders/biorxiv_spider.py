from scrapy import Spider,Request
from biorxiv.items import BiorxivItem
import re

class BiorxivSpider(Spider):
    name='biorxiv_spider'
    start_urls=['https://www.biorxiv.org/collection/cancer-biology?page=0']
    allowed_urls=['https://www.biorxiv.org']

    def parse(self,response):
        num_pages = int(response.xpath('//li[@class="pager-last last odd"]/a/text()').extract_first())
        url_list = [f'https://www.biorxiv.org/collection/cancer-biology?page={i}'
        for i in range(num_pages)]
