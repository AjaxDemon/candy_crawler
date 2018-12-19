# coding: utf-8

import os
import re


def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating project ' + directory)
        os.makedirs(directory)


def create_image_dir(rootdir, subdir='images'):
    pattern = re.compile(r'[?*:"<>\\\/|]')
    subdir = re.sub(pattern, '_', subdir) # 替换windows特殊字符
    directory = os.path.join(rootdir, subdir)
    if not os.path.exists(directory):
        print('Creating image directory ' + directory)
        os.makedirs(directory)
    return directory


def create_data_files(project_name):
    """
    创建临时文件，用于存储爬虫程序中间产生的数据
    * queue.txt 链接队列，初始化状态下，放网站的第一个链接
    * crawled.txt 记录爬虫抓取到的数据
    """
    create_project_dir(project_name)
    queue = os.path.join(project_name, 'queue.txt')
    crawled = os.path.join(project_name, 'crawled.txt')
    if not os.path.isfile(queue):
        write_file(queue, '')
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# 创建一个文件
def write_file(path, data):
    f = open(path, 'wb')
    data = data.encode('utf-8')
    f.write(data)
    f.close()


# 往一个文件里添加内容
def append_to_file(path, data):
    with open(path, 'ab') as file:
        file.write((data+'\n').encode('utf-8'))
        file.close()


# 清理文件内容
def delete_file_contents(path):
    with open(path, 'w'):
        pass


# 读取一个文件的内容，将其中的内容放到set（集合）中
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt', encoding='utf-8') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# 将集合中的数据写入文件
def set_to_file(links, file):
    delete_file_contents(file)
    for link in sorted(links):
        append_to_file(file, link)
