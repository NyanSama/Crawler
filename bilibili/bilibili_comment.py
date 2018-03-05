# encoding: utf-8

"""
@version: v1.0
@author: nyansama
@contact: nyansama@163.com
@software: PyCharm Community Edition
@file: bilibili_comment.py
@time: 2016/12/5 20:32
"""

#from selenium import webdriver
#from selenium.common.exceptions import *
import json
from lxml import html
import requests
import os

class GetBilibiliComment():
    def __init__(self):
        self.browser = webdriver.Chrome()

    def __del__(self):
        self.browser.close()

    def __exit__(self,Type, value, traceback):
        self.browser.close()

    def Getname(self, avnum):
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
            for text, floor in zip(texts, floors):
                floor_num = int(floor.text.strip('#'))
                comment.append(text.text)
                if floor_num == 1:
                    is_next = 0
            if is_next == 0:
                break

            next_b.click()

        for i in comment:
            print (i + '\n')

    ####################
    # use json pkg get comment
    #
    def Getcomment_j(self,num):
        page = 1
        f_name = 'comment/av%d' % num
        f = open(f_name, 'w+')
        while page != -1:
            url = "http://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&sort=0&oid=%d&pn=%d" % (num, page)
            pkg = requests.get(url)
            data = json.loads(pkg.content,encoding='utf-8')

            page += 1
            # print data
            data = data['data']
            total_floor_num = data['page']['count']
            total_user_num = data['page']['acount']
            replies = data['replies']
            for reply in replies:
                u_name = reply['member']['uname']
                u_sign = reply['member']['sign']
                content = reply['content']['message']
                lenth_of_reply = len(reply['replies'])
                if lenth_of_reply:
                    for contents in reply['replies']:
                        r_content = contents['content']['message']
                        content = content + '\n --' + r_content
                floor_num = int(reply['floor'])
                if floor_num == 1:
                    page = -1

                f.write(content.encode('utf-8') + '\n')

def Getcomment_j(num):
    page = 1
    f_name = './comment/av%d' % num
    try:
        print(os.get_exec_path())
    except Exception as identifier:
        print ("DIR already have %s" % identifier)
    f = open('comment.txt', 'wb+')
    while page != -1:
        url = "http://api.bilibili.com/x/v2/reply?jsonp=jsonp&type=1&sort=0&oid=%d&pn=%d" % (num, page)
        pkg = requests.get(url)
        data = json.loads(pkg.content,encoding='utf-8')

        page += 1
        # print data
        data = data['data']
        total_floor_num = data['page']['count']
        total_user_num = data['page']['acount']
        replies = data['replies']
        for reply in replies:
            u_name = reply['member']['uname']
            u_sign = reply['member']['sign']
            content = reply['content']['message']
            lenth_of_reply = len(reply['replies'])
            if lenth_of_reply:
                for contents in reply['replies']:
                    r_content = contents['content']['message']
                    content = content + '\n --' + r_content
            floor_num = int(reply['floor'])
            if floor_num == 1:
                page = -1

            try:
                f.write(content.encode(encoding='utf-8'))
            except Exception as e:
                print(e)
# def func():
#     browser = webdriver.Chrome()
#     browser.get("http://www.bilibili.com/video/av7399194/")
#     browser.implicitly_wait(3)
#     click = browser.find_element_by_xpath('//*[@id="dianji"]').text
#     reviewnum = browser.find_element_by_xpath('//*[@id="dm_count"]').text
#     print click
#     print reviewnum
#     comment_list = []
#     for i in range(5):
#         try:
#             comment_list = browser.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[4]/div[2]/div/ul')
#         except NoSuchElementException as e:
#             browser.implicitly_wait(5)
#
#     if comment_list == []:
#         raise ValueError("no such comment")
#
#     browser.close()
# class Main():
#     def __init__(self):
#         pass







if __name__ == '__main__':
    #test = GetBilibiliComment()
    # test.Getname(7338126)
    #test.Getcomment_j(7338126)
    Getcomment_j(7338126)
