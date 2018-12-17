# coding: utf-8

from urllib.parse import urlparse


def get_domain_name(url):
    try:
        parts = get_sub_domain_name(url).split('.')
        return parts[-2] + '.' + parts[-1]
    except:
        return ''

# 获取域名名称
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
