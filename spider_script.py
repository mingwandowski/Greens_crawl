import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawl import GreensSpider  # Import your Scrapy spider class

def run_spider():
    # Add command-line arguments to the sys.argv list
    sys.argv = ["runspider", "crawl.py", "-o", "/Users/mingwandowski/Developer/greens_crawl/greens.jsonl"]

    process = CrawlerProcess(get_project_settings())
    process.crawl(GreensSpider)  # Replace 'YourSpider' with the actual class name of your spider
    process.start()

if __name__ == '__main__':
    run_spider()

# crontab -e
# * * * * * /opt/homebrew/bin/python3 /Users/mingwandowski/Developer/greens_crawl/spider_script.py  >> /Users/mingwandowski/Developer/greens_crawl/logfile.log 2>&1