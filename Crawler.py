#!/usr/bin/python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URLS_TO_CRAWL = [
    'http://huaban.com/boards/24199444/'
]

CHROME_DRIVER_PATH = 'D:\\Documents\\LightingDeng\\__apps__\\chromedriver.exe'


class Crawler:

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

    def search_candy(self, urls=None):
        if None is urls:
            urls = []
        for url in urls:
            self.driver.get(url)
            elements = []
            ret = self.driver.execute_script('return document.querySelectorAll(".pin a.layer-view");')
            while len(ret) > 0:
                elements.extend(ret)
                el_last_child = self.driver.find_element_by_css_selector('.pin[data-seq]:last-child')
                query = ('max=%s&limit=20&wfl=1' % str(el_last_child.get_attribute('data-seq')))
                self.driver.get('%s?%s' % (url, query))
                ret = self.driver.execute_script('return document.querySelectorAll(".pin a.layer-view");')
                print('%s?%s' % (url, query))
                print('Find elements length: %s' % len(ret))

    @staticmethod
    def run():
        crawler = Crawler()
        crawler.search_candy(URLS_TO_CRAWL)


if __name__ == '__main__':
    Crawler.run()



