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
    本程序利用asyncio进行协程测试
"""

import requests
from bs4 import BeautifulSoup
import configparser
import time, threading, datetime, os, sys, urllib,asyncio
from queue import Queue
from subprocess import call

@asyncio.coroutine
def downloader(data):
    return "Down success!"
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
        data.close()
    except:
        pass

    # future.set_result("down succes!")
    # yield from future
    return "Down success!"


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
    data.close()
    return page

async def urlgetter(site_url, file_dir,a,b):
    # dl.send(None)
    # 可以改进header赋值，尽量避免直接赋值的情况
    url_header = "https://wallpaperscraft.com"
    pages = getpages(site_url)
    if not pages:
        return -1
    for x in pages[a:b]:
        urls = url_header + x
        data = requests.get(urls)
        soup = BeautifulSoup(data.content, 'lxml')
        data.close()
        set = soup.findAll('div', 'wallpaper_pre')
        for i in range(0, len(set)):
            url_t = set[i].findChild().get('href')
            list_t = url_t.split('/')
            name = '_'.join(list_t[-2:]) + '.jpg'
            down_url = url_header + '/image/' + name
            data = [file_dir,down_url]

            # 切协程
            print("DOWNLOAD -- %d -- %d , %s" % (a, i, time.asctime()))
            # future = asyncio.Future()

            result = await asyncio.gather(downloader(data))
            # await asyncio.sleep(a)
            print("DOWLOAD FINISH -- %d-- %d , %s -- %s " % (a, i, time.asctime(), result))






def start():
    type = 'anime'
    size = '2560x1080'
    dirs = 'd:/dowload'
    file_dir = '{dir}/{type}/{size}'.format(dir=dirs, type=type, size=size)
    url = 'https://wallpaperscraft.com/catalog/anime/2560x1080'
    loop = asyncio.get_event_loop()
    task = [
        asyncio.ensure_future(urlgetter(url, file_dir, 5, 6)),
        asyncio.ensure_future(urlgetter(url, file_dir, 6, 7)),
        asyncio.ensure_future(urlgetter(url, file_dir, 4, 5))
    ]
    now = time.time()
    loop.run_until_complete(asyncio.wait(task))





if __name__ == '__main__':
    start()
