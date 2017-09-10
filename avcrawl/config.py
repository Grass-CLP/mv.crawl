from avcrawl.mongomodel import Config

img_path = "S:/imgs/"

Config(_id="img_path", value=img_path).save()
