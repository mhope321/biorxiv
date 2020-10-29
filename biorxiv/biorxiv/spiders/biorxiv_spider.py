from scrapy import Spider,Request
from biorxiv.items import BiorxivItem
import re

class BiorxivSpider(Spider):
    name='biorxiv_spider'
    start_urls=['https://www.biorxiv.org/collection/cancer-biology?page=0']
    allowed_urls=['https://www.biorxiv.']

    def parse(self,response):
        num_pages = int(response.xpath('//li[@class="pager-last last odd"]/a/text()').extract_first())
        url_list = [f'https://www.biorxiv.org/collection/cancer-biology?page={i}'
        for i in range(num_pages)]

        for url in url_list[:2]:
            yield Request(url=url,callback=self.parse_resultpage)

    def parse_resultpage(self,response):
        papers = response.xpath('//a[@class="highwire-cite-linked-title"]/@href').extract()
        papers_url = [f'https://www.biorxiv.org{suffix}' for suffix in papers]

        for url in papers_url[:2]:
            yield Request(url=url,callback=self.parse_paperpage)

    def parse_paperpage(self,response):
        paper_title = response.xpath('//h1[@class="highwire-cite-title"]/text()').extract()
        subject_area = response.xpath('//span[@class="highwire-article-collection-term"]/a/text()').extract()
        doi = response.xpath('//span[@class="highwire-cite-metadata-doi highwire-cite-metadata"]/text()').extract_first()
        date_posted = response.xpath('//div[@class="panel-pane pane-custom pane-1"]/div/text()').extract()
        meta = {'paper_title':paper_title,'subject_area':subject_area,'doi':doi,'date_posted':date_posted}

        article_info_url = response.url+'.article-info'
        yield Request(url=article_info_url,callback=self.parse_infopage,meta=meta)

    def parse_infopage(self,response):
        author_names = response.xpath('//ol[@class="contributor-list"]/li/span[@class="name"]/text()').extract()
        affiliation_nums = response.xpath('//ol[@class="contributor-list"]/li/a/text()').extract()
        affiliation_text = response.xpath('//ol[@class="affiliation-list"]/li/address/text()').extract()
        meta = {'author_names':author_names,'affiliation_nums':affiliation_nums,'affiliation_text':affiliation_text}

        metric_url = response.url.split('.article-info')
        metric_url = metric_url[0]+'.article-metrics'
        yield Request(url=metric_url,callback=self.parse_metricpage,meta=meta)

    def parse_metricpage(self,response):
        downloads = response.xpath('//tbody/tr').extract()

        item = BiorxivItem()
        item['paper_title'] = response.meta['paper_title']
        item['doi'] = response.meta['doi']
        item['date_posted'] = response.meta['date_posted']
        item['subject_area'] = response.meta['subject_area']
        item['author_names'] = response.meta['author_names']
        item['affiliation_nums'] = response.meta['affiliation_nums']
        item['affiliation_text'] = response.meta['affiliation_text']
        item['downloads'] = downloads
        yield item
