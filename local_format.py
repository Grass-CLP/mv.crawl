# coding=utf-8
import os
import re
import shutil

import winshell

from avcrawl.config import format_path, img_path, wait_format_path
from avcrawl.mongomodel import Video

video_ext = ['mp4', 'avi', 'mkv', 'wmv', 'mov', 'mpeg', 'rmvb', 'mp3', 'flv', 'qsv', 'pdf']
img_ext = ['jpg', 'jpeg']

format_root = os.path.join(format_path, "all")
undefined_root = os.path.join(format_root, '_Undefined')
format_role = os.path.join(format_path, "role")
format_score = os.path.join(format_path, "score")
format_images = os.path.join(format_path, "shortcut_img")
for v in [format_root, format_role, format_score, undefined_root]:
    if not os.path.exists(v):
        os.makedirs(v)


def findVideo(name):
    video = None
    code = re.search('([A-Z]{2,6})-?(\d{3,5})', name, re.M | re.I)
    if code is not None:
        avcode = code.group(1).upper() + '-' + code.group(2)
        video = Video.objects(_id=avcode).first()
    return video


def getPath(video, format=["_id"]):
    if video is None:
        return ""

    if len(format) == 0:
        format = ["_id"]

    path = ""
    for key in format:
        if key == "code":
            code = (video._id).split('-')[0]
            path = path + code + '/'
        elif key in video._fields:
            path = path + video[key] + '/'
        else:
            path = path + key + '/'
    return "None" if len(path) == 0 else path[:-1]


def createFormatPath(video, root=format_root, format=["code", "_id"]):
    if video is None:
        return

    relpath = getPath(video, format=format)
    path = os.path.join(root, relpath)
    if not os.path.exists(path):
        os.makedirs(path)

    return path, relpath


def moveAFile(video, file_path):
    target_path, relpath = createFormatPath(video)
    shutil.move(file_path, target_path)
    if os.path.exists(os.path.join(img_path, video.img)):
        shutil.copy(os.path.join(img_path, video.img), target_path)

    # Video.objects(_id=video._id).update_one(set__local_path=target_path)
    return target_path


def moveAImage(video, file_path):
    target_path, relpath = createFormatPath(video)
    try:
        shutil.move(file_path, target_path)
    except:
        pass


def shortcutBuild(video):
    target_path, relpath = createFormatPath(video)

    # role base
    for role in video.roles:
        path = os.path.join(format_role, role["name"])
        if not os.path.exists(path):
            os.makedirs(path)
        winshell.CreateShortcut(
            Path=os.path.join(path, video['_id']) + ".lnk",
            Target=target_path)

    # score base
    score = str(int(0 if video.score is None or video.watch_num < 5 else video.score))
    path = os.path.join(format_score, score)
    if not os.path.exists(path):
        os.makedirs(path)
    winshell.CreateShortcut(
        Path=os.path.join(path, video['_id']) + ".lnk",
        Target=target_path)

    # images
    target_path = os.path.join(img_path, video.img)
    if os.path.exists(target_path) and not os.path.exists(os.path.join(format_images, video['_id'] + ".jpg")):
        shutil.copy(target_path, os.path.join(format_images, video['_id'] + ".jpg"))


def loadAPath(dir, video_type=video_ext, img_type=img_ext):
    for root, dirs, files in os.walk(dir):
        pending_files = files[:]
        video = None
        video_count = 0
        for f in files:
            ext = f[f.rfind('.') + 1:]
            if ext in video_ext:
                # find target to move
                video = findVideo(f)
                if video is not None:
                    video_count += 1
                    moveAFile(video, os.path.join(root.decode('gbk'), f.decode('gbk')))
                else:
                    shutil.move(os.path.join(root.decode('gbk'), f.decode('gbk')), undefined_root)
                pending_files.remove(f)
            elif ext in img_ext:
                # find key code img to move
                video = findVideo(f)
                if video is not None:
                    moveAImage(video, os.path.join(root.decode('gbk'), f.decode('gbk')))
                    pending_files.remove(f)

        files = pending_files[:]
        # if this dir only one video, move all img to format path
        if video is not None and video_count == 1:
            for f in files:
                if f[f.rfind('.') + 1:] in img_ext:
                    moveAImage(video, os.path.join(root.decode('gbk'), f.decode('gbk')))
                    pending_files.remove(f)

        if len(pending_files) == 0 and len(dirs) == 0:
            # shutil.rmtree(root, ignore_errors=True)
            print "delete: " + root.decode('gbk')


def formatVideos():
    # format videos
    for path in wait_format_path:
        loadAPath(path)


def updateLocal():
    # scan local files and set into video
    # Video.objects(_id=video._id).update_one(set__local_path=target_path)
    # format_root > files > ids
    Video.objects().update(unset__local_path=True)
    all_codes = os.listdir(format_root)
    for codes in all_codes:
        codePath = os.path.join(format_root, codes)
        all_code = os.listdir(codePath)
        for code in all_code:
            target_path = os.path.join(codePath, code)
            Video.objects(_id=code).update_one(set__local_path=target_path)


def buildShortcuts():
    # build shortcuts
    shortcut_dirs = [format_role, format_score, format_images]
    for d in shortcut_dirs:
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)

    videos = Video.objects(local_path__exists=True)
    for video in videos:
        shortcutBuild(video)


formatVideos()
updateLocal()
buildShortcuts()
