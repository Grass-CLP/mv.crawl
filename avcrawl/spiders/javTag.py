import scrapy
import time
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import Spider
# from avcrawl.items import Video
from avcrawl.mongomodel import Video, Role


class TagSpider(Spider):
    name = "tag"
    allowed_domains = ["javlibrary.com"]
    start_urls = [
        # "http://dmoztools.net/Computers/Software/Operating_Systems/Object-Oriented",
        "http://www.javlibrary.com/cn/genres.php",
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=('Languages',))),
    #     Rule(LinkExtractor(allow=('Python/',)), callback='parse_item'),
    # )

    def parse(self, response):
        groupsEle = response.css('div.textbox')
        item = dict()
        item['_id'] = "tags" + time.strftime("%Y-%m-%d", time.localtime())
        item['_type'] = 'tags'
        groups = []
        for gEle in groupsEle:
            group = dict()
            group = {
                "_id": gEle.css('div.boxtitle::text').extract_first(),
                "tags": gEle.css('a::text').extract(),
            }
            groups.append(group)
        item['data'] = groups

        yield item


Role.objects(rank__exists=True).update(unset__rank=True)
