#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/6.
# email to LipsonChan@yahoo.com
#

import time
from scrapy.spiders import Spider
from avcrawl.mongomodel import Role


class RoleSpider(Spider):
    name = "role"
    allowed_domains = ["javlibrary.com"]
    start_urls = [
        # "http://dmoztools.net/Computers/Software/Operating_Systems/Object-Oriented",
        "http://www.javlibrary.com/cn/star_mostfav.php",
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=('Languages',))),
    #     Rule(LinkExtractor(allow=('Python/',)), callback='parse_item'),
    # )

    def parse(self, response):
        starsEle = response.css('div.starbox div.searchitem')
        item = dict()
        item['code'] = "role" + time.strftime("%Y-%m-%d", time.localtime())
        item['_type'] = 'roles'
        stars = []
        for starEle in starsEle:
            star = {
                "code": starEle.css('::attr(id)').extract_first(),
                "rank": int(starEle.css('h3::text').extract_first()[1:]),
                "img": starEle.css('img::attr(src)').extract_first(),
                "name": starEle.css('img::attr(title)').extract_first(),
            }
            stars.append(star)
        item['data'] = stars

        yield item


Role.objects(rank__exists=True).update(unset__rank=True)
