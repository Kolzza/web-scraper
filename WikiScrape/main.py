from spiders.WikiScraper import WebScraper
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from config import LOGGING, LOG_LEVEL, SPIDER_COUNT
from utils import get_arguments, read_seed_urls, split_list


def main():
    seed_file, max_files, max_depth, output_dir = get_arguments()
    seed_urls = split_list(read_seed_urls(seed_file), SPIDER_COUNT)

    settings = get_project_settings()
    settings.set('LOG_ENABLED', LOGGING)
    settings.set('LOG_LEVEL', LOG_LEVEL)
    settings.set('OUTPUT_DIR', output_dir)
    settings.set('DEPTH_LIMIT', int(max_depth))
    settings.set('GLOBAL_ITEM_LIMIT', int(max_files))

    process = CrawlerProcess(settings)
    for idx, url_list in enumerate(seed_urls):
        process.crawl(WebScraper, id=idx, start_urls=url_list, allowed_domains=['wikipedia.org'])
    process.start()


if __name__ == "__main__":
    main()
