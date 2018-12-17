# coding: utf-8

from urllib.request import urlopen, Request, HTTPError
from general import *
from candy_finder import CandyFinder
from image_loader import ImageLoader

class Spider:

    # 类变量
    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    image_dir = ''
    queue = set()
    crawled = set()
    headers = {}

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = os.path.join(project_name, 'queue.txt')
        Spider.crawled_file = os.path.join(project_name, 'crawled.txt')
        Spider.image_dir = os.path.join(project_name, 'images')
        
        Spider.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

        self.boot()
        # self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name)
        create_image_dir(Spider.project_name)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url, page_index=0):
        if page_url not in Spider.crawled:
            print('[' + thread_name + '] now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | Crawled ' + str(len(Spider.crawled)))
            result = Spider.gather_link(page_url)
            if 0 == len(result):
                return False
            else:
                Spider.add_links_to_queue(result)
                Spider.update_files()
                return True

    @staticmethod
    def gather_link(page_url):
        html_string = ''
        try:
            links = set()
            page_idx = 1
            
            while True:
                pattern = re.compile(r'_\d+\.html') # 替换html页，以分页结尾
                if 1 == page_idx:
                    page_url = re.sub(pattern, '.html', page_url)
                else: 
                    page_url = re.sub(pattern, '_'+str(page_idx)+'.html', page_url)
                
                req = Request(url=page_url, headers=Spider.headers)
                response = urlopen(req)

                if 'text/html' == response.getheader('content-type'):
                    html_bytes = response.read()
                    html_string = html_bytes.decode('utf-8')
                    
                    link = CandyFinder.get_candy(html_string)
                    pattern = re.compile(r'/>$') # 添加排序
                    link = re.sub(pattern, ' sort="' + str(page_idx)+'"/>', link)
                    links.add(link)
                else: continue
                page_idx += 1
        except HTTPError as e:
            print('Error: page_url ', page_url)
            print('Error: can not craw page, ', e)
        finally:
            return links

    @staticmethod
    def add_links_to_queue(links):
        for link in links:
            url = CandyFinder.candy_info(link)['url']
            if link in Spider.queue:
                continue
            if link in Spider.crawled:
                continue
            Spider.queue.add(link)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)

    @staticmethod
    def crawl_image(thread_name, link):
        try:
            if link in Spider.crawled:
                print('Image is crawled, quit.', link)
                return
            info = CandyFinder.candy_info(link)
            print('[' + thread_name + '] now download image ' + info['name'] + ', url: ' + info['url'])
            file_path = create_image_dir(Spider.image_dir, info['name'])
            ImageLoader.grab(file_path, info['url'], info['sort']+'.jpg')
            Spider.queue.remove(link)
            Spider.crawled.add(link)
            Spider.update_files()
        except BaseException as e:
            print('Error: crawl image failed, ', e)

