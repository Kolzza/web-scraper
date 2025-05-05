import scrapy


class WebScraper(scrapy.Spider):
    name="wikipedia"
    visited=set()

    def parse(self, response):
        url = response.url
        print(url, "is URL!!!")
        if url in self.visited:
            return
        self.visited.add(url)
        
        yield { 
            'body': response.body,
            'url': url
        }

        for link in response.css('div.mw-parser-output a::attr(href)'):
            if link.startswith('/wiki/') and ':' not in link:
                full_url = response.urljoin(link)
                if full_url not in self.visited:
                    print("Yielding", full_url)
                    yield scrapy.Request(url=full_url, callback=self.parse)
