# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from scrapy import signals
from scrapy.exceptions import DropItem
import os


class WikiscrapePipeline:
    item_count = 0
    spiders = set()
    stopped = False

    @classmethod
    def from_crawler(cls, crawler):
        p = cls()
        p.output_dir = crawler.settings.get('OUTPUT_DIR', 'out')
        p.item_limit = crawler.settings.getint('GLOBAL_ITEM_LIMIT', 100)

        crawler.signals.connect(p.spider_opened, signal=signals.spider_opened)
        return p

    @classmethod
    def spider_opened(cls, spider):
        cls.spiders.add(spider)

    def _limit_reached(self):
        return WikiscrapePipeline.item_count >= self.item_limit
    
    def _shutdown_spiders(self):
        WikiscrapePipeline.stopped = True
        for s in WikiscrapePipeline.spiders:
            s.crawler.engine.close_spider(s, f"Global item limit reached: {self.item_limit}")

    def _write_output(self, item):
        filename = os.path.join(self.output_dir, f"{item['url'].split('/')[-1]}.html")
        with open(filename, 'wb') as file:
            file.write(item['body'])

    def process_item(self, item, spider):
        if self._limit_reached():
            raise DropItem
        
        WikiscrapePipeline.item_count += 1
        if not WikiscrapePipeline.stopped and self._limit_reached():
            self._shutdown_spiders()
        
        self._write_output(item)

        return item
