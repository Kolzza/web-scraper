# cs172

## Quick Start
1. Create a text file with your seed URLs, or modify `seeds.txt`
   ```
   https://en.wikipedia.org/wiki/List_of_search_engines
   https://en.wikipedia.org/wiki/Volcano
   ...
   ```

2. Run the `crawler.sh` script
   ```
   ./crawler.sh <Seed File> <File Limit> <Max Hops> <Output Directory>
   ```
   or `crawler.bat` on Windows
   ```
   .\crawler.sh <Seed File> <File Limit> <Max Hops> <Output Directory>
   ```

## Advanced Configuration
Additional settings for the crawler can be modified via the `WikiScrape/config.py`.

### Disable Logging
Scrapy's verbose logging is disabled by default to keep the command line output clean
```
LOGGING="False"
```
### Log Level
To enable and customize logging, set a desired log level (e.g., "INFO", "DEBUG").
Refer to [Scrapy log levels](https://docs.scrapy.org/en/latest/topics/logging.html#log-levels) for more options.
```
LOG_LEVEL="INFO"
```
### Spider Count
Define how many spiders run concurrently. Default is 2.
```
SPIDER_COUNT=2
```
### Domain Whitelist
Limit crawling to specific domains. An empty list disables filtering.
```
WHITELIST=['wikipedia.org']
```
For further customization, edit `WikiScrape/settings.py`. See the [Scrapy settings guide](https://docs.scrapy.org/en/latest/topics/settings.html) for full details.
