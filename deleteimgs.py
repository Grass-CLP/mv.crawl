import os

from avcrawl.config import img_path
from avcrawl.mongomodel import Video

vs = Video.objects(imgs__gt=[])
for video in vs:
    imgs = video.imgs
    for img in imgs:
        file = os.path.join(img_path, img)
        # print file
        if os.path.exists(file):
            os.remove(file)

print "end"