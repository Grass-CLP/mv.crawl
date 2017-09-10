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

from avcrawl.mongomodel import *


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
        if item['_type'] == 'video':
            if item['img']:
                url = item['img']
                yield scrapy.Request(url)
            for image_url in item['imgs']:
                yield scrapy.Request(image_url)
        if item['_type'] == 'role':
            yield item

    def item_completed(self, results, item, info):
        if len(results) == 0:
            return item

        if item['_type'] == 'video':
            # deal img
            ok, img = results[0]
            if ok:
                item['img'] = img['path']
            del results[0]

            # deal imgs
            file_paths = [x['path'] for ok, x in results if ok]
            item['imgs'] = file_paths

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
        if item['_type'] == 'video':
            video = Video.objects(_id=item['_id']).first()
            if video is None:
                video = Video(_id=item['_id'])

            # deal with tags
            tags = []
            for t in item['tags']:
                tag = Tag.objects(_id=t['_id']).first()
                if tag is None:
                    tag = Tag(_id=t['_id'])
                update_dynamic_doc(tag, t)
                tag.save()
                tags.append(tag)
            del item['tags']
            video['tags'] = tags

            # deal with role
            roles = []
            for rd in item['roles']:
                role = Role.objects(_id=rd['_id']).first()
                if role is None:
                    role = Role(_id=rd['_id'])
                update_dynamic_doc(role, rd)
                role.save()
                roles.append(role)
            del item['roles']
            video['roles'] = roles

            update_dynamic_doc(video, item)
            video.save()
        return item
