#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/6.
# email to LipsonChan@yahoo.com
#

from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class VideoSpider(CrawlSpider):
    name = "video"
    allowed_domains = ["javlibrary.com"]
    start_urls = [
        "http://www.javlibrary.com/cn/vl_bestrated.php",
        "http://www.javlibrary.com/cn/vl_mostwanted.php",

        # "http://www.javlibrary.com/cn/",
        # "http://www.javlibrary.com/cn/star_mostfav.php",
        #
        # "http://www.javlibrary.com/cn/vl_bestrated.php",
        # "http://www.javlibrary.com/cn/vl_update.php",
        #
        # "http://www.javlibrary.com/cn/vl_mostwanted.php",
        # "http://www.javlibrary.com/cn/vl_newentries.php",
        # "http://www.javlibrary.com/cn/vl_newrelease.php",
        #
        # "http://www.javlibrary.com/cn/genres.php",
    ]

    rules = (
        Rule(LinkExtractor(allow='vl_star\.php')),
        Rule(LinkExtractor(allow=('vl_bestrated\.php', 'vl_update\.php'))),
        Rule(LinkExtractor(allow=('vl_mostwanted\.php', 'vl_newentries\.php', 'vl_newrelease\.php'))),
        Rule(LinkExtractor(allow='vl_genre\.php\?')),
        Rule(LinkExtractor(allow=('cn\/\?v=',)), callback='parse_video'),
    )

    # rules = (
    #     Rule(LinkExtractor(allow=('Languages',))),
    #     Rule(LinkExtractor(allow=('Python/',)), callback='parse_item'),
    # )

    def parse_video(self, response):
        info = response.css('#video_jacket_info')
        # video = Video()
        # video._id = info.css("div#video_id td.text::text").extract_first()
        # video.img = info.css("#video_jacket_img::attr(src)").extract_first()
        # video.save()

        # video._id = info.css("div#video_id td.text::text").extract_first()
        # video.title = response.css("div#video_title a::text").extract_first()
        # video.img = info.css("#video_jacket_img::attr(src)").extract_first()
        # if video.img:
        #     video.img = u'http:' + video.img
        # video.date = info.css("div#video_date td.text::text").extract_first()
        # video.length = info.css("div#video_length span.text::text").extract_first()
        # video.marker = info.css("div#video_length span.marker a::text").extract_first()
        # video.label = info.css("div#video_label span.label a::text").extract_first()
        # score = info.css("div#video_review span.score::text").extract_first()
        # video.score = float(score[1:-1])
        # video.type = info.css("div#video_genres span.genre a::text").extract()
        # video.role = info.css("div#video_cast span.cast a::text").extract()
        # video.want_num = response.css("span#subscribed a::text").extract_first()
        # video.watch_num = response.css("span#watched a::text").extract_first()
        # video.had_num = response.css("span#owned a::text").extract_first()
        # video.imgs = response.css("div.previewthumbs img::attr(src)").extract()
        # video.comments = response.css("table.comment td.t textarea::text").extract()

        video = dict()
        video['_type'] = 'video'
        video['code'] = info.css("div#video_id td.text::text").extract_first()
        video['title'] = response.css("div#video_title a::text").extract_first()
        video['img'] = info.css("#video_jacket_img::attr(src)").extract_first()
        if video['img']:
            video['img'] = u'http:' + video['img']
        video['date'] = info.css("div#video_date td.text::text").extract_first()
        video['length'] = info.css("div#video_length span.text::text").extract_first()
        video['marker'] = info.css("div#video_maker span.maker a::text").extract_first()
        video['label'] = info.css("div#video_label span.label a::text").extract_first()
        score = info.css("div#video_review span.score::text").extract_first()
        video['score'] = 0 if score is None else float(score[1:-1])
        video['tags'] = info.css("div#video_genres span.genre a::text").extract()

        # parse role
        roleEle = info.css("span.cast")
        roles = []
        for r in roleEle:
            _id = r.css("span.star a::attr(href)").extract_first()
            if _id:
                _id = _id[_id.rfind('=') + 1:]
                role = {
                    "code": _id,
                    "name": r.css("span.star a::text").extract_first(),
                    "alias": r.css("span.alias::text").extract_first(),
                }
                roles.append(role)
        video['roles'] = roles

        # video['role'] = info.css("div#video_cast span.cast a::text").extract()
        video['want_num'] = response.css("span#subscribed a::text").extract_first()
        video['watch_num'] = response.css("span#watched a::text").extract_first()
        video['had_num'] = response.css("span#owned a::text").extract_first()
        video['imgs'] = response.css("div.previewthumbs img::attr(src)").extract()
        video['comments'] = response.css("table.comment td.t textarea::text").extract()

        # parse
        def toNum(v, name):
            v[name] = 0 if v[name] is None else int(v[name])

        toNum(video, 'length')
        toNum(video, 'had_num')
        toNum(video, 'watch_num')
        toNum(video, 'want_num')
        video['date'] = None if video['date'] is None else datetime.strptime(video['date'], "%Y-%m-%d")

        yield video
        # return video

    # def parse_f(self, response):
    #     sites = response.css('#site-list-content > div.site-item > div.title-and-desc')
    #     items = []
    #     self.time += 1
    #     if self.time > 100:
    #         return
    #
    #     for site in sites:
    #         item = Website()
    #         item['name'] = site.css(
    #             'a > div.site-title::text').extract_first().strip()
    #         item['url'] = site.xpath(
    #             'a/@href').extract_first().strip()
    #         item['description'] = site.css(
    #             'div.site-descr::text').extract_first().strip()
    #         items.append(item)
    #         print items
    #         yield items
    #
    #     for href in response.css("#see-also-content > div.see-also-row > a::attr('href')"):
    #         url = response.urljoin(href.extract())
    #         yield scrapy.Request(url)

    # def parse_dir_contents(self, response):
    #     for sel in response.xpath('//ul/li'):
    #         item = Website()
    #         item['title'] = sel.xpath('a/text()').extract()
    #         item['link'] = sel.xpath('a/@href').extract()
    #         item['desc'] = sel.xpath('text()').extract()
    #         yield item
