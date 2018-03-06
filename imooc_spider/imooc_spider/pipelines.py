# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline

class ImoocSpiderPipeline(object):
    def __init__(self):
        self.file = open('data.json', 'w')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

class ImgPipeline(ImagesPipeline):
    #通过抓取图片的url获取一个Request用于下载
    def get_media_requests(self, course, info):
        yield scrapy.Request(course['image_url'])

    def item_completed(self, results, course, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem("Item contains no images")
        course['image_path'] = image_path
        return course
