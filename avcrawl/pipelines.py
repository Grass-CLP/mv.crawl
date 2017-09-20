# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

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
        if item['code'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['code'])
            return item


class MyImagesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item['_type'] == 'video':
            if item['img']:
                url = item['img']
                yield scrapy.Request(url)
            # for image_url in item['imgs']:
            #     yield scrapy.Request(image_url)

        if item['_type'] == 'roles':
            for star in item['data']:
                img_url = star['img'].replace('http', 'https')
                yield scrapy.Request(img_url)

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

        if item['_type'] == 'roles':
            i = 0
            roles = item['data']
            for ok, x in results:
                roles[i]['img'] = x['path'] if ok else ""
                i += 1

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
            video = Video.objects(code=item['code']).first()
            if video is None:
                video = Video(code=item['code'])

            # deal with role
            roles = []
            for rd in item['roles']:
                role = Role.objects(code=rd['code']).first()
                if role is None:
                    role = Role(code=rd['code'])
                update_dynamic_doc(role, rd)
                role.save()
                roles.append(role)
            del item['roles']
            video['roles'] = roles

            # deal with download
            download = video['download'] if hasattr(video, "download") else []
            comments = []
            for dl in item['comments']:
                if dl.find('ed2k://') != -1 or dl.find('magnet:') != -1:
                    # try to get real download
                    if dl not in download:
                        download.append(dl)
                elif dl.find('http') == -1:
                    # delete noise download, keep real comment
                    comments.append(dl)
            item['comments'] = comments
            video['download'] = download

            update_dynamic_doc(video, item)
            video.save()

        if item['_type'] == 'roles':
            for rd in item['data']:
                role = Role.objects(code=rd['code']).first()
                if role is None:
                    role = Role(code=rd['code'])
                update_dynamic_doc(role, rd)
                role.save()

        if item['_type'] == 'tags':
            for g in item['data']:
                tg = TagGroup(code=g['code'])
                tg.tags = g['tags']
                tg.save()

        return item
