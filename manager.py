#   HOW RUNNIT
# python3 manager.py [output-title] [urls-file] [toxicwords-file] [num-clusters]
import sys
import numpy as np
import pandas as pd

# WEBSCRAPER
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.webscraper import IndeedSpider as Spider

# PREPROCESSING
from preprocessing.preprocessor import preprocessor
from preprocessing.stopwords import stopwords

# ANALYZING
from analyzing.analytics import analytics

title = sys.argv[1]+".csv"
url_file = sys.argv[2]
toxicwords_file = sys.argv[3]
num_clusters = sys.argv[4].split('-')

def scraper():
    url = []
    for line in open(url_file, 'r').readlines():
            url.append(line.strip())

    process = CrawlerProcess({
        'FEED_FORMAT': 'csv',
        'FEED_URI': "db/"+title
    })

    process.crawl(Spider, start_urls=url)
    process.start()

# Generating DB by scrapping proccess
#print("\n>Scraper initalizing...\n")
#scraper()
#print("\n>Scraper done!")

# Preprocessing
print("\n>Preprocessing...\n")
pd = preprocessor(title).run()
print("\n>Preprocessing done!")

# Analytics
print("\n>Analytics...")
print("Processing clusters:")
model = analytics(pd, stopwords("PTBR").get(toxicwords_file))

if len(num_clusters)>1:
    for r in range(int(num_clusters[0]), (int(num_clusters[1])+1)):
        model.run(r, title)
else:
    model.run(int(num_clusters[0]), title)

print("\n>Analytics done!")

