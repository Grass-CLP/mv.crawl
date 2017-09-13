from avcrawl.mongomodel import Config


def loadConf(name, defualt, force = False):
    if force:
        Config(_id=name, value=defualt).save()
        return defualt

    obj = Config.objects(_id=name).first()
    value = defualt
    if obj is not None:
        value = obj.value
    else:
        Config(_id=name, value=value).save()
    return value


def saveConf(name, value):
    Config(_id=name, value=value).save()


img_path = loadConf('img_path', "S:/imgs/")
format_path = loadConf('format_path', 'S:/all_H_video/')
wait_format_path = loadConf('wait_format_path', ['S:/all/'], force = True)
