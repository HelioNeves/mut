import scrapy

class IndeedSpider(scrapy.Spider):
    page_list = []
    name = "Spider"
    start_urls = []
  
    def parse(self, response):
        SET_SELECTOR = '.jobsearch-SerpJobCard'
        for job in response.css(SET_SELECTOR):
            CARD_SELECTOR = '.title a::attr(href)'
            yield response.follow(job.css(CARD_SELECTOR).extract_first(), 
                    callback=self.parse_summary)
        
        NEXT_PAGE_SELECTOR = '.pagination a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR)[-1].extract()
        if (next_page is not None) and not (next_page in IndeedSpider.page_list):
            IndeedSpider.page_list.append(next_page)
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

    def parse_summary(self, response):
        TITLE_SELECTOR = '.jobsearch-JobInfoHeader-title ::text'
        COMPANY_SELECTOR = '.jobsearch-DesktopStickyContainer-companyrating ::text'
        SUMMARY_SELECTOR = '.jobsearch-jobDescriptionText *::text'
        yield {
            'title': response.css(TITLE_SELECTOR).extract_first(),
            'company': response.css(COMPANY_SELECTOR).extract_first(),
            'summary': response.css(SUMMARY_SELECTOR).extract()
        }        

