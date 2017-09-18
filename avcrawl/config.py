from avcrawl.mongomodel import Config


def loadConf(name, defualt, force = False):
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


img_path = loadConf('img_path', "S:/imgs/")
format_path = loadConf('format_path', 'S:/all_H_video/')
wait_format_path = loadConf('wait_format_path',
                            [
                                'S:/other/',
                                'S:/download/',
                                'S:/package/',
                                # 'S:/jav/',
                             ],
                            force = True)
