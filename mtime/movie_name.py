# encoding: utf-8

"""
@version: v1.0
@author: nyansama
@contact: nyansama@163.com
@software: PyCharm Community Edition
@file: movie_name.py.py
@time: 2016/12/6 18:53
"""
import sys
# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
# from PyQt4.QtWebKit import *
from lxml import html
from selenium import webdriver
from selenium.common.exceptions import *
import json
import time
import random

# class Render(QWebPage):
#     def __init__(self, url):
#         self.app = QApplication(sys.argv)
#         QWebPage.__init__(self)
#         self.loadFinished.connect(self._loadFinished)
#         self.mainFrame().load(QUrl(url))
#         self.app.exec_()
#
#     def _loadFinished(self, result):
#         self.frame = self.mainFrame()
#         self.app.quit()

# def func1():
#     name = []
#
#     for i in range(1,3):
#         f_html = open('test.html', 'w')
#         url = "http://movie.mtime.com/movie/search/section/#pageIndex=%d&nation=138" % i
#         r = Render(url)
#         result = r.frame.toHtml()
#         f_result = str(result.toUtf8())
#         f_html.write(f_result)
#         f_html.close()
#         tree = html.fromstring(f_result)
#         archive_links1 = tree.xpath('//*[@id="searchResultRegion"]/ul/*/div[1]/div/div[2]/h3/a/text()')
#         archive_links2 = tree.xpath('//*[@id="searchResultRegion"]/ul/*/div[2]/div/div[2]/h3/a/text()')
#         name.append(archive_links1)
#         name.append(archive_links2)
#
#     name_file = open('name','a+')
#     for i in name:
#         for j in i :
#             name_file.write(j.encode('utf-8')+'\n')
#
#     name_file.close()
#     f_html.close()

class GetmovieName():
    def __init__(self):
        self.browser  = webdriver.Chrome()
    def __del__(self):
        self.browser.close()
    def __exit__(self):
        self.browser.close()

    def getname(self):
        name = []
        fname = open('name2', 'a+')
        for i in range(1,690):
            url = "http://movie.mtime.com/movie/search/section/#pageIndex=%d&nation=138" % i
            self.browser.get(url)
            self.browser.refresh()
            time.sleep(int(random.random()*5+5))
            name_list = self.browser.find_elements_by_xpath('//*[@id="searchResultRegion"]/ul/*/div[1]/div/div[2]/h3/a')
            name_list.extend( self.browser.find_elements_by_xpath('//*[@id="searchResultRegion"]/ul/*/div[2]/div/div[2]/h3/a'))

            for element in name_list:
                # name.append(element.text.encode('utf-8'))
                fname.write(element.text.encode('utf-8')+'\n')
                fname.close()
                fname = fname = open('name2','a+')

        fname.close()
        return name


    def get_info(self):
        info = []
        detail_list = []
        for i in range(1,690):
            url = "http://movie.mtime.com/movie/search/section/#pageIndex=%d&nation=138" % i
            self.browser.get(url)
            self.browser.refresh()
            time.sleep(int(random.random()*10+5))
            div_list = self.browser.find_elements_by_xpath('//*[@id="searchResultRegion"]/ul/*')
            for divs in div_list:
                mov1 = divs.find_element_by_xpath('div[1]')
                mov2 = divs.find_element_by_xpath('div[2]')
                detail_list.append(self.get_detail(mov1))
                detail_list.append(self.get_detail(mov2))

    def get_detail(self,element):
        """
        :param element:
        :return:
        :type element: selenium.webdriver.remote.webelement.WebElement
        """
        name = element.find_element_by_xpath('div/div[2]/h3/a').text.encode('utf-8')
        score = element.find_element_by_xpath('div/div[2]/div/p/span[1]').text.encode('utf-8') + element.find_element_by_xpath('div/div[2]/div/p/span[2]').text.encode('utf-8')
        p_num = element.find_element_by_xpath('div/div[2]/p[3]').text.encode('utf-8')[0:-6]
        year = element.find_element_by_xpath('div/div[2]/h3/span').text.encode('utf-8').strip('()')
        en_name = element.find_element_by_xpath('div/div[2]/p[1]/a').text.encode('utf-8')
        detail = name + ',' + en_name + ',' + score + ',' + p_num + ',' + year
        return detail





if __name__ == '__main__':
    page = GetmovieName()

    names = page.getname()






