import scrapy

class WebScraper(scrapy.Spider):
    name="wikipedia"
    visited=set()

    def start_requests(self):
        self.url_queue = []
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f"out/{self.name}/{response.url.split('/')[-1]}.html"
        with open(filename, 'wb') as f:
            f.write(response.body)

        for link in response.css('div.mw-parser-output ul li a'):
            text = link.css('::text').get()
            href = link.css('::attr(href)').get()
            if text and href:
                full_url = response.urljoin(href)
                if full_url not in WebScraper.visited:
                    self.url_queue.append(full_url)
                    WebScraper.visited.add(full_url)
                yield {
                    'text': text,
                    'href': full_url
                }

        while self.url_queue:
            next_url = self.url_queue.pop(0)
            yield scrapy.Request(url=next_url, callback=self.parse)


        
    