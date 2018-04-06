#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/6.
# email to LipsonChan@yahoo.com
#

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class AvcrawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Video(Item):
    _id = Field()
    title = Field()
    img = Field()
    date = Field()
    length = Field()
    marker = Field()
    label = Field()
    score = Field()
    type = Field()
    role = Field()
    want_num = Field()
    watch_num = Field()
    had_num = Field()
    imgs = Field()
    comments = Field()
