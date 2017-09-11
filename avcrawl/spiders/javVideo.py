import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy.spiders import Spider
# from avcrawl.items import Video
from avcrawl.mongomodel import Video


class VideoSpider(Spider):
    name = "video"
    allowed_domains = ["javlibrary.com"]
    start_urls = [
        # "http://dmoztools.net/Computers/Software/Operating_Systems/Object-Oriented",
        "http://www.javlibrary.com/cn/?v=javlillg7i",
        "http://www.javlibrary.com/cn/?v=javliitcze",
    ]

    # rules = (
    #     Rule(LinkExtractor(allow=('Languages',))),
    #     Rule(LinkExtractor(allow=('Python/',)), callback='parse_item'),
    # )

    def parse(self, response):
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
        video['_id'] = info.css("div#video_id td.text::text").extract_first()
        video['title'] = response.css("div#video_title a::text").extract_first()
        video['img'] = info.css("#video_jacket_img::attr(src)").extract_first()
        if video['img']:
            video['img'] = u'http:' + video['img']
        video['date'] = info.css("div#video_date td.text::text").extract_first()
        video['length'] = info.css("div#video_length span.text::text").extract_first()
        video['marker'] = info.css("div#video_length span.marker a::text").extract_first()
        video['label'] = info.css("div#video_label span.label a::text").extract_first()
        score = info.css("div#video_review span.score::text").extract_first()
        video['score'] = float(score[1:-1])

        #parse tags
        tagsEle = info.css("div#video_genres span.genre")
        tags = []
        for t in tagsEle:
            id = t.css("a::attr(href)").extract_first()
            if id:
                id = id[id.rfind('=') + 1:]
                tag = {
                    "_id" : id,
                    "name" : t.css("a::text").extract_first(),
                }
                tags.append(tag)
        video['tags'] = tags
        # video['tags'] = info.css("div#video_genres span.genre a::text").extract()

        # parse role
        roleEle = info.css("span.cast")
        roles = []
        for r in roleEle:
            id = r.css("span.star a::attr(href)").extract_first()
            if id:
                id = id[id.rfind('=') + 1:]
                role = {
                    "_id" : id,
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
        #prase

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
