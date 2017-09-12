from avcrawl.mongomodel import Config


def loadConf(name, defualt):
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
