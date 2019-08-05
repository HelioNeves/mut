#   HOW RUN IT
# python3 webscraper.py [db-title] [urls-file]
import sys
import numpy as np
import pandas as pd

# WEBSCRAPER
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.webscraper import IndeedSpider as Spider

# ARGS
title = sys.argv[1] + ".csv"
url_file = sys.argv[2]


def scraper():
    url = []
    for line in open(url_file, "r").readlines():
        url.append(line.strip())

    process = CrawlerProcess({"FEED_FORMAT": "csv", "FEED_URI": "db/" + title})

    process.crawl(Spider, start_urls=url)
    process.start()


# Generating DB by scrapying proccess
print("\n>Scraper initalizing...\n")
scraper()
print("\n>Scraper done!")
