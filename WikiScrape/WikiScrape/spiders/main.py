import scrapy

class WebScraper(scrapy.Spider):
    name = "scraper"
    start_urls = ['https://en.wikipedia.org/wiki/List_of_search_engines']

    def __init__(self, seeds=None):
        _seeds = seeds
        _queue = []

   
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): 
        for link in response.css('div.mw-parser-output ul li a'):
            text = link.css('::text').get()
            href = link.css('::attr(href)').get()
            if text and href:
                yield {
                    'text': text,
                    'href': response.urljoin(href)  
                }  
            
        
        
    