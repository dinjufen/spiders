from scrapy.spiders import Spider
import sys
from scrapy import Request
from imp import reload
sys.path.append("..")
reload(sys)
from items import ImoocSpiderItem

class imooc_spider(Spider):
    #用于区别Spider
    name = "imooc_spider"
    #允许访问的域
    allowed_domains = ["imooc.com"]
    #爬取的网址
    start_urls = ["http://www.imooc.com/course/list"]

    #爬取方法
    def parse(self, response):
        #实例一个容器保存爬取的信息
        course = ImoocSpiderItem()
        for box in response.xpath("//div[@class='course-card-container']/a[@target='_blank']"):
            course['url'] = "http://www.imooc.com" + box.xpath('.//@href').extract()[0]
            # print(course['url'].decode('utf-8'))
            course['title'] = box.xpath('.//h3/text()').extract()[0].strip()
            # print(course['title'].decode('utf-8'))
            course['image_url'] = 'http:'+ box.xpath('.//@src').extract()[0]
            course['student'] = box.xpath(".//div[@class='course-card-info']/span/text()").extract()[1]
            # print(course['student'].decode('utf-8'))
            course['introduction'] = box.xpath('.//p/text()').extract()[0].strip()
            # print(course['introduction'].decode('utf-8'))
            yield course

        #下一页url跟进
        url = response.xpath("//a[contains(text(),'下一页')]/@href").extract()
        if url:
            page = "http://www.imooc.com" + url[0]
            #将请求返回给parse自身处理
            yield Request(page, callback=self.parse)
