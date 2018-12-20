#!/usr/bin/python
# -*- coding:utf-8 -*-

import threading
import time
import json
from queue import Queue
from lib.Logger import Log, Logger
from lib.Spider import Spider


class CandyCrawler:

    def __init__(self, options):
        self.crawl_page_threads = options['crawl_page_threads']
        self.down_image_threads = options['down_image_threads']
        self.webdriver_path = options['webdriver_path']
        self.resource_dir = options['resource_dir']
        self.rootlink_queue = Queue()
        self.sublink_queue = Queue()
        self.image_queue = Queue()
        self.create_crawl_page_workers()
        self.create_down_image_workers()

    def create_crawl_page_workers(self):
        for _ in range(self.crawl_page_threads):
            t = threading.Thread(target=self.rootlink_work)
            t.daemon = True
            t.start()
        for _ in range(self.crawl_page_threads):
            t = threading.Thread(target=self.sublink_work)
            t.daemon = True
            t.start()

    def create_down_image_workers(self):
        for _ in range(self.crawl_page_threads):
            t = threading.Thread(target=self.down_image_work)
            t.daemon = True
            t.start()

    def rootlink_work(self):
        logger = Log()
        spider = Spider(self.resource_dir, logger=logger, webdriver_path=self.webdriver_path)
        current_thread = threading.current_thread().name
        wait_times = 0
        while True:
            if self.rootlink_queue.empty():
                logger.write('[%s] No root page to crawl, waiting...' % current_thread)
                time.sleep(2*wait_times)
                wait_times += 1
                if wait_times > 10:
                    break
                continue
            else:
                wait_times = 0
            logger.record('[%s] Thread start: crawl_rootlink' % current_thread)
            url = self.rootlink_queue.get()
            try:
                next_rootlink, sublinks = spider.crawl_rootlink(url)
                if next_rootlink is not None:
                    self.rootlink_queue.put(next_rootlink)
                for sublink_object in sublinks:
                    self.sublink_queue.put(sublink_object)
                self.rootlink_queue.task_done()
            except BaseException as error:
                logger.write_error_trace('[%s] Caught exception:' % current_thread, error=error)
                self.rootlink_queue.put(url)
                self.rootlink_queue.task_done()
            logger.write_to_file()

    def sublink_work(self):
        logger = Log()
        spider = Spider(self.resource_dir, logger=logger, webdriver_path=self.webdriver_path)
        current_thread = threading.current_thread().name
        wait_times = 0
        while True:
            if self.sublink_queue.empty():
                logger.write('[%s] No sub page to crawl, waiting...' % current_thread)
                time.sleep(2*wait_times)
                wait_times += 1
                if wait_times > 10:
                    break
                continue
            else:
                wait_times = 0
            logger.record('[%s] Thread start: crawl_sublink' % current_thread)
            sublink_object = self.sublink_queue.get()
            try:
                imagelink_object = spider.crawl_sublink(sublink_object)
                self.image_queue.put(imagelink_object)
                self.sublink_queue.task_done()
            except BaseException as error:
                logger.write_error_trace('[%s] Caught exception:' % current_thread, error=error)
                self.sublink_queue.put(sublink_object)
                self.sublink_queue.task_done()
            logger.write_to_file()

    def down_image_work(self):
        logger = Log()
        spider = Spider(self.resource_dir, logger=logger, webdriver_path=self.webdriver_path)
        current_thread = threading.current_thread().name
        wait_times = 0
        while True:
            if self.image_queue.empty():
                logger.write('[%s] No sub page to crawl, waiting...' % current_thread)
                time.sleep(2*wait_times)
                wait_times += 1
                if wait_times > 10:
                    break
                continue
            else:
                wait_times = 0
            logger.record('[%s] Thread start: crawl_image' % current_thread)
            image_object = self.image_queue.get()
            try:
                spider.crawl_image(image_object)
                self.image_queue.task_done()
            except BaseException as error:
                logger.write_error_trace('[%s] Caught exception:' % current_thread, error=error)
                self.image_queue.put(image_object)
                self.image_queue.task_done()
            logger.write_to_file()

    def boot(self, links):
        for rootlink in links:
            self.rootlink_queue.put(rootlink)
            Logger.write('Put rootlink:', rootlink)
            self.rootlink_queue.join()
            self.sublink_queue.join()
            self.image_queue.join()

    @staticmethod
    def run():
        config = CandyCrawler.load_config_file('config.json')
        crawler = CandyCrawler(config)
        crawler.boot(config['boards'])

    @staticmethod
    def load_config_file(filename='config_resource.json'):
        Logger.write('Loading config file:', filename)
        with open(filename, 'r', encoding='utf8') as file:
            config_json = json.load(file)
            Logger.write('Load success, content: \n'+json.dumps(config_json))
            file.close()
        return config_json


if __name__ == '__main__':
    start = time.time()
    CandyCrawler.run()
    print('Execute OK, %is' % (time.time() - start))

