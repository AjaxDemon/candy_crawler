#!/usr/bin/python
# coding: utf-8

import threading
import time
import math
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = ''
HOMEPAGE = ''
SID_START_FROM = 10000
TASK_GOAL = 10100


DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = os.path.join(PROJECT_NAME, 'queue.txt')
CRAWLED_FILE = os.path.join(PROJECT_NAME, 'crawled.txt')
NUMBER_OF_THREADS = 8
DOWNIMG_THREADS = math.floor(NUMBER_OF_THREADS/2)
CRAWPAGE_THREADS = NUMBER_OF_THREADS - DOWNIMG_THREADS
page_queue = Queue()
image_queue = Queue()



Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def create_crawpage_workers():
    for _ in range(CRAWPAGE_THREADS):
        t = threading.Thread(target=crawpage_work)
        t.daemon = True
        t.start()

def create_downimg_workers():
    for image in file_to_set(QUEUE_FILE):
        image_queue.put(image)
    for _ in range(DOWNIMG_THREADS):
        t = threading.Thread(target=downimg_work)
        t.daemon = True
        t.start()
    image_queue.join()

def crawpage_work():
    current_thread = threading.current_thread().name
    while True:
        if page_queue.empty():
            print('[' + current_thread + '] No page to craw, waiting...')
            time.sleep(1)
            continue
        sid = page_queue.get()
        Spider.crawl_page(current_thread, os.path.join(HOMEPAGE, str(sid) + '_1.html'))
        for image in file_to_set(QUEUE_FILE):
            image_queue.put(image)
        page_queue.task_done()

def downimg_work():
    current_thread = threading.current_thread().name
    while True:
        if image_queue.empty():
            print('[' + current_thread + '] No image to download, waiting...')
            time.sleep(1)
            continue
        link = image_queue.get()
        Spider.crawl_image(current_thread, link)
        image_queue.task_done()


def link_producer():
    sid = SID_START_FROM
    while sid < TASK_GOAL:
        sid += 1
        page_queue.put(sid)
        print('Put ', sid, ' into queue')
        if 0 == page_queue.qsize() % CRAWPAGE_THREADS:
            print('Wait for worker complete...')
            page_queue.join()
            print('Worker completed queue')
        print('Producer sleep 1s...')
        time.sleep(1)
    print('Producer is done, wait for worker complete...')
    page_queue.join()
    image_queue.join()

# create_crawpage_workers()
create_downimg_workers()
# link_producer()
