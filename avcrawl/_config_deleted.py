#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2018/4/6.
# email to LipsonChan@yahoo.com
#

from avcrawl.mongomodel import Config


def loadConf(name, defualt, force=False):
    if force:
        Config(code=name, value=defualt).save()
        return defualt

    obj = Config.objects(code=name).first()
    value = defualt
    if obj is not None:
        value = obj.value
    else:
        Config(code=name, value=value).save()
    return value


def saveConf(name, value):
    Config(code=name, value=value).save()


_proxy_conf = loadConf('proxy', 'http://127.0.0.1:49328')
_img_path = loadConf('img_path', "S:/imgs/")
_format_path = loadConf('format_path', 'S:/all_H_video/')
_wait_format_path = loadConf('wait_format_path',
                            [
                                'S:/other/',
                                'S:/download/',
                                'S:/package/',
                                # 'S:/jav/',
                            ],
                            force=True)
