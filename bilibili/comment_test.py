# encoding: utf-8

"""
@version: v1.0
@author: nyansama
@contact: nyansama@163.com
@software: PyCharm Community Edition
@file: comment_test.py
@time: 2016/12/5 20:32
"""

from selenium import webdriver
from selenium.common.exceptions import *
import json
from lxml import html
import requests

class GetBilibiliComment():
    def __init__(self):
        self.browser  = webdriver.Chrome()
    def __del__(self):
        self.browser.close()
    def __exit__(self):
        self.browser.close()

    def Getname(self,avnum):
        url = "http://www.bilibili.com/video/av%d" % avnum
        self.browser.get(url)
        self.browser.implicitly_wait(3)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.browser.implicitly_wait(5)
        comment = []
        is_next = 1
        page = 1
        total_page = 100000
        while is_next == 1:
            # try find nextPage
            try:
                box = self.browser.find_element_by_class_name("pagelistbox")
                elements = box.find_elements_by_xpath('*')
                next_b = elements[-1]
            except NoSuchElementException as e:
                is_next = 0

            comment_list = self.browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[4]/div[2]/div/ul')
            texts = comment_list.find_elements_by_xpath('*/div[3]')
            floors = comment_list.find_elements_by_xpath('*/div[4]/span[1]')
            for text,floor in zip(texts,floors):
                floor_num = int(floor.text.strip('#'))
                comment.append(text.text)
                if floor_num == 1:
                    is_next = 0
            if is_next == 0:
                break

            next_b.click()

        for i in comment:
            print i + '\n'




def func():
    browser = webdriver.Chrome()
    browser.get("http://www.bilibili.com/video/av7399194/")
    browser.implicitly_wait(3)
    click = browser.find_element_by_xpath('//*[@id="dianji"]').text
    reviewnum = browser.find_element_by_xpath('//*[@id="dm_count"]').text
    print click
    print reviewnum
    comment_list = []
    for i in range(5):
        try:
            comment_list = browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[4]/div[2]/div/ul')
        except NoSuchElementException as e:
            browser.implicitly_wait(5)

    if comment_list == []:
        raise ("no suck comment")

    browser.close()


# class Main():
#     def __init__(self):
#         pass

def GetComment_j(num):
    page = 1
    while page!= 0:
        url = "http://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&sort=0&oid=%d&pn=%d" % (num,page)
        pkg = requests.get(url)
        data = json.loads(pkg.content,'utf-8')

        print data





if __name__ == '__main__':
    # test = GetBilibiliComment()
    # test.Getname(7338126)
    GetComment_j(7338126)