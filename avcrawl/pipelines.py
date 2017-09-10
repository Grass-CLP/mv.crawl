# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
import scrapy

from avcrawl.mongomodel import Video, update_document, update_dynamic_doc


class AvcrawlPipeline(object):
    def process_item(self, item, spider):
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['_id'])
            return item


class MyImagesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item['img']:
            url = item['img']
            #item.img =
            yield scrapy.Request(url)
        for image_url in item['imgs']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        return item


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):
        valid = True
        if type(item) != dict:
            raise DropItem('Missing{0}!'.format(item))
        if valid:
            # download img
            video = Video.objects(_id=item['_id']).first()
            if video is None:
                video = Video()
            # update_dynamic_doc(video, item)
            # video.save()
            pass

            # deal with role

            # item.save()

            # self.collection.insert(dict(item))
            # log.msg('question added to mongodb database!',
            #         level=log.DEBUG, spider=spider)
        return item
