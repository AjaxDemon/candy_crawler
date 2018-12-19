# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lib.FileHelper import create_image_dir
from lib.Logger import Log
from lib.ImageLoader import ImageLoader


class Spider:

    driver = None

    def __init__(self, resource_dir, logger=None, webdriver_path=None):
        if logger is not None:
            self.logger = logger
        else:
            self.logger = Log()
        self.resource_dir = resource_dir
        self.driver = self.make_chrome_webdriver(webdriver_path)
        self.logger.write('webdrivaer_path', webdriver_path)

    def make_chrome_webdriver(self, webdriver_path):
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
            return webdriver.Chrome(chrome_options=chrome_options, executable_path=webdriver_path)
        else:
            return self.driver

    def crawl_rootlink(self, url):
        sublinks = set()
        self.driver.get(url)
        board_name = self.driver.find_element_by_css_selector('.board-name').text
        image_dir = create_image_dir('%s/%s' % (self.resource_dir, board_name))

        ret = self.driver.execute_script('return document.querySelectorAll(".pin a.layer-view");')
        while len(ret) > 0:
            for element in ret:
                sublinks.add({
                    'image_dir': image_dir,
                    'sublink': element.get_attribute('href')
                })
            el_last_child = self.driver.find_element_by_css_selector('.pin[data-seq]:last-child')
            query = ('max=%s&limit=20&wfl=1' % str(el_last_child.get_attribute('data-seq')))
            self.driver.get('%s?%s' % (url, query))
            ret = self.driver.execute_script('return document.querySelectorAll(".pin a.layer-view");')
            self.logger.record('Request root page %s?%s' % (url, query))
        self.logger.record('Found sub page size: %s' % len(sublinks))

        return sublinks

    def crawl_sublink(self, object):
        self.driver.get(object['sublink'])
        el_img = self.driver.find_element_by_css_selector('.zoom-layer img')
        object['imagelink'] = el_img.get_attribute('src')
        self.logger.record('Found image link: %s' % object['imagelink'])
        return object

    def crawl_image(self, object):
        self.logger.record('Grab link: %s' % object['imagelink'])
        ImageLoader.grab(object['image_dir'], object['imagelink'])

