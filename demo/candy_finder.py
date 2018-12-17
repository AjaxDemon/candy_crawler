# coding: utf-8

from bs4 import BeautifulSoup

class CandyFinder:

    PARSER = 'html.parser'

    @staticmethod
    def get_candy(html_string):
        soup = BeautifulSoup(html_string, CandyFinder.PARSER)
        candy = soup.find(id='imgString').find('img')
        print('candy: ', candy)
        return str(candy)

    @staticmethod
    def candy_info(candy):
        soup = BeautifulSoup(candy, CandyFinder.PARSER)
        img = soup.find('img')
        return {'name': img['alt'], 'url': img['src'], 'sort': img['sort']}
