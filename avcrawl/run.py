#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/6.
# email to LipsonChan@yahoo.com
#

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from avcrawl.spiders.javVideo import VideoSpider

runner = CrawlerRunner(get_project_settings())
d = runner.crawl(VideoSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()

# process = CrawlerProcess(get_project_settings())
# process.crawl(VideoSpider)
# process.start()
