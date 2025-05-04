# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import os


class WikiscrapePipeline:

    @classmethod
    def from_crawler(cls, crawler):
        p = cls()
        p.output_dir = crawler.settings.get('OUTPUT_DIR', 'out')
        return p

    def process_item(self, item, spider):
        filename = os.path.join(self.output_dir, f"{item['url'].split('/')[-1]}.html")
        with open(filename, 'wb') as file:
            file.write(item['body'])

        return item
