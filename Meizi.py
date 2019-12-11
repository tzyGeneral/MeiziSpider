import requests
import os
import time
from usrAgent import UserAgent
import random
import re
from lxml import etree


class MeiziSpider:
    def __init__(self):
        self.url = 'https://www.mzitu.com/all/'
        self.headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205',
            'Referer': 'https://www.toutiao.com'
        }
        self.refererUrl = 'https://www.mzitu.com/all/'

    def getHtml(self, url):
        try:
            self.headers['User-Agent'] = UserAgent().random_userAgent()
            response = requests.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                return response
        except:
            return None

    def re_func(self, re_bds, html):
        pattern = re.compile(re_bds, re.S)
        r_list = pattern.findall(html)
        return r_list

    def getHrefUrl(self):
        html = self.getHtml(self.url)
        if html:
            parse_obj = etree.HTML(html.text)
            href_list = parse_obj.xpath('//div[@class="all"]/ul[@class="archives"]/li/p[@class="url"]/a/@href')
            print("href_list:", href_list)
            for href in href_list:
                yield href

    def save_image(self, url):
        self.headers['Referer'] = self.refererUrl
        i = 0
        while True:
            try:
                img_link = url + '/{}'.format(i)
                html = self.getHtml(img_link)

                re_bds = ' <div class="main-image"><p><a href="https://www.mzitu.com/.*?" ><img ' \
                         'src="(.*?)" alt="(.*?)" width=".*?" height=".*?" /></a></p>'
                img_html_list = self.re_func(re_bds, html.text)

                name = img_html_list[0][1]
                print('正在下载 -> {}'.format(name))
                direc = './图片/{}'.format(name)

                imgData = self.getHtml(img_html_list[0][0])

                imgData = imgData.content
                filename = direc + name + img_link.split('/')[-1] + '.jpg'
                with open(filename, 'wb') as f:
                    f.write(imgData)
                i += 1
            except Exception as e:
                self.refererUrl = url
                print(e)
                break

    def runSpider(self):
        for url in self.getHrefUrl():
            self.save_image(url)


if __name__ == "__main__":
    spider = MeiziSpider()
    spider.runSpider()


