#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading
import time
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lib.Spider import Spider
from lib.Logger import Log

URLS_TO_GRAB = [
    'http://huaban.com/boards/49815866/',
    'http://huaban.com/boards/17890318/',
    'http://huaban.com/boards/22195009/',
    'http://huaban.com/boards/31288587/',
]

RESOURCE_DIR = 'resource'

CHROME_DRIVER_PATH = 'D:\\Documents\\LightingDeng\\__apps__\\chromedriver.exe'


class ThreadWebdriver:

    driver = None
    image_queue = None
    page_queue = None

    def __init__(self, number_of_threads=2, webdriver_path=CHROME_DRIVER_PATH):
        self.image_queue = Queue()
        self.page_queue = Queue()
        self.webdriver_path = webdriver_path
        for _ in range(number_of_threads):
            t = threading.Thread(target=self.crawl_page)
            t.daemon = True
            t.start()
        for _ in range(number_of_threads):
            t = threading.Thread(target=self.grab_image)
            t.daemon = True
            t.start()

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
            return webdriver.Chrome(chrome_options=chrome_options, executable_path=self.webdriver_path)
        else:
            return self.driver

    def crawl_page(self):
        logger = Log()
        spider = Spider(RESOURCE_DIR, logger=logger, webdriver_path=CHROME_DRIVER_PATH)
        current_thread = threading.current_thread().name
        wait_times = 0
        while True:
            if self.page_queue.empty():
                logger.write('[%s] No page to crawl, waiting...' % current_thread)
                wait_times += 1
                time.sleep(2*wait_times)
                if wait_times > 10:
                    break
                continue
            else:
                wait_times = 0
            url = self.page_queue.get()
            try:
                next_rootlink, objects = spider.crawl_rootlink(url)
                if next_rootlink is not None:
                    self.page_queue.put(next_rootlink)
                for obj in objects:
                    self.image_queue.put(obj['sublink'])
                self.page_queue.task_done()
            except BaseException as error:
                logger.write_error_trace('[%s] Caught exception:' % current_thread, error=error)
                self.page_queue.task_done()
            logger.write_to_file()

    def grab_image(self):
        logger = Log()
        driver = self.make_chrome_webdriver()
        current_thread = threading.current_thread().name
        wait_times = 0
        while True:
            if self.image_queue.empty():
                logger.write('[%s] No image to grab, waiting...' % current_thread)
                wait_times += 1
                time.sleep(2*wait_times)
                if wait_times > 10:
                    break
                continue
            else:
                wait_times = 0
            url = self.image_queue.get()
            try:
                driver.get(url)
                el_img = self.driver.find_element_by_css_selector('.zoom-layer img')
                imagelink = el_img.get_attribute('src')
                print('Grab image: ', imagelink)
                self.image_queue.task_done()
            except BaseException as error:
                logger.write_error_trace('[%s] Caught exception:' % current_thread, error=error)
                self.image_queue.task_done()
            logger.write_to_file()

    def boot(self, urls=URLS_TO_GRAB):
        for i in urls:
            self.page_queue.put(i)
        self.page_queue.join()
        self.image_queue.join()

    @staticmethod
    def run():
        tw = ThreadWebdriver()
        tw.boot()

if __name__ == '__main__':
    ThreadWebdriver.run()

