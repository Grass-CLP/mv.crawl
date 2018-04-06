import os

from avcrawl.mongomodel import Video
from config import img_path

vs = Video.objects(imgs__gt=[])
for video in vs:
    imgs = video.imgs
    for img in imgs:
        file = os.path.join(img_path, img)
        # print file
        if os.path.exists(file):
            os.remove(file)

print "end"
