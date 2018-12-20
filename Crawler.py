#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lib.Logger import Logger
from lib.ImageLoader import ImageLoader
from lib.FileHelper import *

URLS_TO_CRAWL = [
    'http://huaban.com/boards/17890318/',
]

CHROME_DRIVER_PATH = 'D:\\Documents\\LightingDeng\\__apps__\\chromedriver.exe'


class Crawler:

    resource_path = 'resource'
    driver = None

    def __init__(self):
        self.driver = self.make_chrome_webdriver()

    def make_chrome_webdriver(self):
        """
        创建headless的chrome webdriver驱动
        :return:
        """
        if None is self.driver:
            chrome_options = Options()
            # 无头模式启动
            chrome_options.add_argument('--headless')
            # 谷歌文档提到需要加上这个属性来规避bug
            chrome_options.add_argument('--disable-gpu')
            # 初始化实例
            return webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROME_DRIVER_PATH)
        else:
            return self.driver

    def search_and_grab_candy(self, urls=None):
        if None is urls:
            urls = []
        for url in urls:
            self.driver.get(url)
            board_name = self.driver.find_element_by_css_selector('.board-name').text
            image_dir = create_image_dir('%s/%s' % (self.resource_path, board_name))

            suburls = []
            ret = self.driver.execute_script('return document.querySelectorAll(".pin a.layer-view");')
            while len(ret) > 0:
                for element in ret:
                    suburls.append(element.get_attribute('href'))
                el_last_child = self.driver.find_element_by_css_selector('.pin[data-seq]:last-child')
                query = ('max=%s&limit=20&wfl=1' % str(el_last_child.get_attribute('data-seq')))
                self.driver.get('%s?%s' % (url, query))
                ret = self.driver.execute_script('return document.querySelectorAll(".pin a.layer-view");')
                Logger.record_log('Request root url page %s?%s' % (url, query))
                Logger.write_log_file()
            Logger.record_log('Find suburls length: %s' % len(suburls))

            imgurls = []
            for suburl in suburls:
                self.driver.get(suburl)
                el_img = self.driver.find_element_by_css_selector('.zoom-layer img')
                imgurls.append(el_img.get_attribute('src'))
                Logger.record_log('Request sub url page %s' % el_img.get_attribute('src'))
                Logger.write_log_file()
            Logger.record_log('Find imgurls length: %s' % len(imgurls))

            for imgurl in imgurls:
                Logger.record_log('Grab: %s' % imgurl)
                ImageLoader.grab(image_dir, imgurl)

            Logger.write_log_file()

    @staticmethod
    def run():
        crawler = Crawler()
        crawler.search_and_grab_candy(URLS_TO_CRAWL)


if __name__ == '__main__':
    start = time.time()
    Crawler.run()
    print('Execute OK, %is' % (time.time() - start))
