#!/usr/bin/env python
# encoding: utf-8


"""
@version: python3.5
@author: ‘miaomiao‘
@contact: nyansama@163.com
@site: http://www.nyansama.cn
@software: PyCharm Community Edition
@file: WS_yield.py
@time: 2017/9/25 15:47
@PS:
    本程序利用send/yield进行测试
"""

import requests
from bs4 import BeautifulSoup
import configparser
import time, threading, datetime, os, sys, urllib
from queue import Queue
from subprocess import call


def downloader():
    result = None
    while True:
        data = yield result
        file_dir = data[0]
        down_site = data[1]
        try:
            if not file_dir and not down_site:
                return
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_path = file_dir + '/' + down_site.split('/')[-1]
            data = requests.get(down_site)
            with open(file_path, 'wb') as f:
                f.write(data.content)
            result = 0
        except:
            result = -1


def getpages(url):
    print("GET PAGES...")
    page = []
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'lxml')
    pages = soup.find('div', 'pages')
    if not pages:
        return None
    lists = pages.findChildren('a')
    try:
        total_page = int(lists[-1].get_text())
    except:
        return None
    if total_page <= 1:
        return page
    tmp_url = lists[-1].get('href').split('/')
    pre = '/'.join(tmp_url[:-1])
    page.append(pre + '#')
    for i in range(2, total_page):
        sub = '/' + 'page%d' % i
        page.append(pre + sub)

    return page


def urlgetter(dl, site_url, file_dir):
    dl.send(None)
    # 可以改进header赋值，尽量避免直接赋值的情况
    url_header = "https://wallpaperscraft.com"
    pages = getpages(site_url)
    if not pages:
        return -1
    for x in pages[0:1]:
        urls = url_header + x
        data = requests.get(urls)
        soup = BeautifulSoup(data.content, 'lxml')
        set = soup.findAll('div', 'wallpaper_pre')
        for i in range(0, len(set)):
            url_t = set[i].findChild().get('href')
            list_t = url_t.split('/')
            name = '_'.join(list_t[-2:]) + '.jpg'
            down_url = url_header + '/image/' + name
            # 切协程

            print("DOWNLOAD -- %d , %s" % (i, time.asctime()))
            result = dl.send([file_dir, down_url])
            print("DOWLOAD FINISH -- %d , %s" % (i, time.asctime()))
    dl.close()


def start():
    type = 'anime'
    size = '2560x1080'
    dirs = 'd:/dowload'
    file_dir = '{dir}/{type}/{size}'.format(dir=dirs, type=type, size=size)

    url = 'https://wallpaperscraft.com/catalog/anime/2560x1080'

    dl = downloader()
    urlgetter(dl, url, file_dir)


if __name__ == '__main__':
    start()
