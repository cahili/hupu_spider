#!/usr/bin/env python
# coding=utf-8
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Qynh(object):
    """docstring for Qynh"""

    def __init__(self, start_url):
        self.start_url = start_url
        self.file_path = r'C:/Users/Administrator/Desktop/image1/'
        self.black_list = ['http://i3.hoopchina.com.cn/blogfile/201607/15/BbsImg146856695084284_990x350.jpg',
                           'http://i2.hoopchina.com.cn/blogfile/201607/14/BbsImg146848226267170_990x1468.jpg',
                           'http://i3.hoopchina.com.cn/blogfile/201607/15/BbsImg146856691730986_990x350.jpg',
                           'http://i3.hoopchina.com.cn/blogfile/201607/14/BbsImg146849026577472_600x445.jpg']

    def spider(self, url):
        r = requests.get(url)
        r.encoding = 'gbk'
        html_doc = r.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        return soup

    def get_image(self):
        n = 0
        dc = {}
        for page in range(1, 3):
            url = self.start_url.format(page)
            soup = self.spider(url)
            tr_ = soup.select(
                "html body div.hp-wrap div#container div#container_nopadd div#search_main div.search_topic_list table.mytopic.topiclisttr tbody tr")
            for tr in tr_:
                td = tr.find_all('td')
                autor = td[2].get_text()
                link_ = td[0].a
                link = link_['href']
                soup1 = self.spider(link)
                div = soup1.find('div', class_='floor_box')
                img_ = div.find_all(
                    'img', src="http://b1.hoopchina.com.cn/web/sns/bbs/images/placeholder.png")
                for img in img_:
                    image_url = img['data-original']
                    if image_url in self.black_list:
                        continue
                    n = n + 1
                    autorname = autor + '{}.jpg'.format(n)
                    dc[autorname] = image_url
        return dc

    def save_image(self):
        dc = self.get_image()
        for autorname in dc:
            link = dc[autorname]
            res = requests.get(link, stream=True)
            with open(self.file_path + autorname, 'wb') as fd:
                print autorname
                for chunk in res.iter_content():
                    fd.write(chunk)

if __name__ == '__main__':
    Qynhimage = Qynh(
        "http://my.hupu.com/search?q=%C7%F2%D2%C2%C5%AE%BA%A2%B5%DA2%BC%BE&type=s_subject&sortby=postdate&fid=34&page={}")
    Qynhimage.save_image()
