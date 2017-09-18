from avcrawl.mongomodel import *

vs = Video.objects()
for v in vs:
    v.roles_bk = v.roles
    v.roles = []
    v.save()
#TODO
