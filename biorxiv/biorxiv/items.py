# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiorxivItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    paper_title = scrapy.Field()
    doi = scrapy.Field()
    date_posted = scrapy.Field()
    subject_area = scrapy.Field()
    author_names = scrapy.Field()
    affiliation_nums = scrapy.Field()
    affiliation_text = scrapy.Field()
    number_of_tweets = scrapy.Field()
    number_of_comments = scrapy.Field()
    number_of_downloads = scrapy.Field()
