import sys
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.webscraper import IndeedSpider as Spider

title = sys.argv[1]+".csv"
url_file = "scraper/"+sys.argv[2]

url = []
for line in open(url_file, 'r').readlines():
        url.append(line.strip())

process = CrawlerProcess({
    'FEED_FORMAT': 'csv',
    'FEED_URI': title
})

process.crawl(Spider, start_urls=url)
process.start()
