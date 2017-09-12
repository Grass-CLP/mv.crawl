from scrapy.crawler import CrawlerProcess
from avcrawl.spiders.javVideo import VideoSpider

process = CrawlerProcess()
process.crawl(VideoSpider)
process.start()

# scrapy crawl video