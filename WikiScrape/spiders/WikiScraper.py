import scrapy


class WebScraper(scrapy.Spider):
    name="wikipedia"
    visited=set()

    def parse(self, response):
        url = response.url
        if url in self.visited:
            return
        self.visited.add(url)
        
        yield { 
            'body': response.body,
            'url': url
        }

        for link in response.css('div.mw-parser-output a::attr(href)'):
            href = link.get()
            if href and href.startswith('/wiki/') and ':' not in href:
                full_url = response.urljoin(href)
                if full_url not in self.visited:
                    yield scrapy.Request(url=full_url, callback=self.parse)
