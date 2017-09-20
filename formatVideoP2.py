from avcrawl.mongomodel import *
from datetime import datetime

# Video.objects().update(unset__imgs=True)
vs = Video.objects()

for v in vs:
    if type(v.date) == datetime:
        continue
    v.watch_num = 0 if v.watch_num is None else int(v.watch_num)
    v.length = 0 if v.watch_num is None else int(v.length)
    v.had_num = 0 if v.watch_num is None else int(v.had_num)
    v.want_num = 0 if v.watch_num is None else int(v.want_num)
    v.date = datetime.strptime(v.date, "%Y-%m-%d")
    v.roles = v.roles_bk
    v.roles_bk = None
    v.save()

