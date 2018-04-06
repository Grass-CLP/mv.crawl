# 影片目录重建项目

## 说明
* 本项目本为个人学习爬虫及兴趣所写，切勿乱传。
* 为协助广大宅男半开放，需要一定编程能力
* 功能1：爬虫爬电影数据
* 功能2：根据爬虫爬到的电影数据及**本地影像文件名**，按照一定目录结构整理本地文件夹，识别不出会单独存放
* 基于python2.7,windows

## 依赖 
* mongodb
* win32api ```https://github.com/mhammond/pywin32/releases```
* python包: scrapy, winshell, pillow

## 环境准备
* windows
* ss (网址需要翻越great wall)
* win32api

## 爬虫运行
* 配置config.py中的代理信息及mongodb地址(自行建立collection)
* 确保mongodb运行，所有配置正确
* 抓取tag,存储数据到mongodb，运行```scrapy crawl tag```
* 抓取role(演员)，运行```scrapy crawl role```
* 抓取video(重点)，配置avcrawl/spides/javVideo.py中的start_urls，运行```scrapy crawl video```
* 爬虫抓取为幂等操作，可自行修改为可自动回复上次爬虫状态

## 本地文件夹整理
* 不推荐不熟悉代码的朋友使用该功能
* 配置config.py中的路径信息
* img_path存放抓取的图片原图，抓取太多的话会存储很大。30m部会有60G
* wait_format_path存放所有原始影响文件,待处理，处理完会移动所有文件及删除所有不必要文件
* format_path存放所有格式化好的目录结果，强烈要求与wait_format_path同个盘
* 确保mongodb运行
* 运行```python local_format.py```

