import requests
from fake_useragent import UserAgent
import urllib.parse
from random import random
from bs4 import BeautifulSoup
import time


class TieBaImageSpider:
    def __init__(self, begin_page, end_page, headers, tie_ba_name, filename):
        self.begin_page = begin_page
        self.end_page = end_page
        self.headers = headers
        self.tie_ba_name = tie_ba_name
        self.filename = filename

    def tie_ba_spider(self):  # 获取贴吧页面内容
        url = r'http://tieba.baidu.com/f?'
        for page in range(self.end_page):
            pn = page*50
            keyword = {'kw': self.tie_ba_name, 'pn': pn}
            kw = urllib.parse.urlencode(keyword)
            tie_ba_url = url + kw   # 构造贴吧每一页的url
            # 设置重连次数
            requests.adapters.DEFAULT_RETRIES = 5
            # 设置连接活跃状态为False
            s = requests.session()
            s.keep_alive = False
            result = requests.get(tie_ba_url, self.headers).text
            self.link_spider(result)

    def link_spider(self, result):  # 解析页面贴子链接
        soup = BeautifulSoup(result, 'lxml')
        links = soup.select('div[class="threadlist_lz clearfix"] a[class="j_th_tit "]')
        for link in links:
            # print(link.attrs["href"])
            content_link = r'http://tieba.baidu.com' + link.attrs["href"]  # 构造帖子的链接
            # print(content_link)
            self.image_spider(content_link)

    def image_spider(self, content_link):  # 获取帖子内容并解析图片链接
        time.sleep(random())
        # 设置重连次数
        requests.adapters.DEFAULT_RETRIES = 5
        # 设置连接活跃状态为False
        s = requests.session()
        s.keep_alive = False
        res = requests.get(content_link, self.headers).text   # 获取帖子的内容
        soup_1 = BeautifulSoup(res, 'lxml')
        image_links = soup_1.select('img[class="BDE_Image"]')  # 解析帖子里图片的链接
        for img_link in image_links:
            # print(image_link.attrs["src"])
            image_link = img_link.attrs["src"]    # 图片的链接
            self.write_image(image_link)

    def write_image(self, image_link):
        time.sleep(random())
        # 设置重连次数
        requests.adapters.DEFAULT_RETRIES = 5
        # 设置连接活跃状态为False
        s = requests.session()
        s.keep_alive = False
        image_content = requests.get(image_link, self.headers).content  # 图片的内容
        print('正在存储图片：', self.filename, '....')
        with open(r'D:\Python\python\tieba_image_spider1\\' + str(self.filename) + '美女.jpg', 'wb') as f:
            f.write(image_content)   # 以二进制的形式存入本地
        self.filename += 1


def main():
    begin_page = 1
    end_page = 20
    ua = UserAgent()
    headers = {'UseAgent': ua.random}
    tie_ba_name = '美女'
    filename = 1
    tie_ba_image_spider = TieBaImageSpider(begin_page, end_page, headers, tie_ba_name, filename)
    tie_ba_image_spider.tie_ba_spider()


if __name__ == '__main__':
    main()
