import scrapy
import os

class WebScraper(scrapy.Spider):
    name = "scraper"
    start_urls = ['https://en.wikipedia.org/wiki/List_of_search_engines']
    _queue = []
    def __init__(self, seeds=None):
        _seeds = seeds
        _queue = []

   
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        output_dir = "out"
        os.makedirs(output_dir, exist_ok=True)

        filename = os.path.join(output_dir, f"{self.name}_{response.url.split('/')[-1]}.html")
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        for link in response.css('div.mw-parser-output ul li a'):
            text = link.css('::text').get()
            href = link.css('::attr(href)').get()
            if text and href:
                full_url = response.urljoin(href)
                self._queue.append(full_url)
                yield {
                    'text': text,
                    'href': full_url
                }  
        while self._queue:
            next_url = self._queue.pop(0)
            yield scrapy.Request(url=next_url, callback=self.parse)