#!/usr/bin/env python
# encoding: utf-8


"""
@version: python3.5
@author: ‘miaomiao‘
@contact: nyansama@163.com
@site: http://www.nyansama.cn
@software: PyCharm Community Edition
@file: WS_mult_asyncio.py
@time: 2017/9/27 15:10
@PS :
     本程序试用asyncio 及 multiprocessing 包进行多进程并行及协程并发异步IO操作
"""

from bs4 import BeautifulSoup
import requests, os, sys, time
import multiprocessing
import asyncio

now = lambda :time.time()

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


async def downloader(data):
    # return "Down Success!"
    file_dir = data[0]
    down_site = data[1]
    try:
        if not file_dir and not down_site:
            return
        file_path = file_dir + '/' + down_site.split('/')[-1]
        data = requests.get(down_site)
        if data.status_code != 200:
            print("Requests Error : %s" % data.status_code)
            return
        with open(file_path, 'wb') as f:
            f.write(data.content)
        data.close()
    except Exception as e:
        return "Down Failed : %s" % e
    return "Down Success!"


async def page_down(site_url, file_dir,page_num):
    data = requests.get(site_url)
    if data.status_code != 200:
        print("Requests Error : %s" % data.status_code)
        return
    soup = BeautifulSoup(data.content, 'lxml')
    data.close()
    set = soup.findAll('div', 'wallpaper_pre')
    if not set:
        print ("NO Wallpaper_pre")
    for i in range(0, len(set)):
        # 使用href中的链接，即图片中的详情链接进行名称提取
        url_t = set[i].findChild().get('href')
        list_t = url_t.split('/')
        name = '_'.join(list_t[-2:]) + '.jpg'
        down_url = 'https://wallpaperscraft.com/image/' + name
        data = [file_dir, down_url]

        # 切协程
        # print("DOWNLOAD -- page %d --%d, %s" % (page_num, i, time.asctime()))
        result = await asyncio.gather(asyncio.ensure_future(downloader(data)))
        # await asyncio.sleep(a)
        # print("FINISHED -- page %d -- %d, %s -- %s" % (page_num, i, time.asctime(),result[0]))


def start_asyncio(pages,file_dir,i):
    url_header = 'https://wallpaperscraft.com'
    tasks = []
    count = 0

    print("[--]Asyncio loop %d Begin --" % i)
    begin = now()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for page in pages:
        task_url = url_header + page
        count = count + 1
        tasks.append(asyncio.ensure_future(page_down(task_url, file_dir, count)))

    loop.run_until_complete(asyncio.wait(tasks))
    print("[--]Asyncio loop %d Finished --" % i)
    print("[--]Asyncio loop %d Total time : %d --" % (i,now()-begin))



def start_mltp(settings):
    # 初始化变量
    type = settings['type']
    size = settings['size']
    dirs = settings['path']
    file_dir = '{dir}/{type}/{size}'.format(dir=dirs, type=type, size=size)
    url = 'https://wallpaperscraft.com/catalog/{type}/{size}'.format(type=type, size=size)
    url_header = 'https://wallpaperscraft.com'

    process_num = 4

    # 初始化文件夹
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    #获取页面长度
    pages = getpages(url)
    if not pages:
        print("GET PAGES Failed ")
    print("[--]GET PAGES success ")
    page_len = len(pages)

    # 初始化 task list
    task = []
    sub_page = []

    # 计算任务列表数
    for i in range(process_num-1):

        begin = i * int(page_len/process_num)

        end = (i+1) * int(page_len/process_num) - 1

        sub_page = pages[begin:end]
        # 启动进程
        p = multiprocessing.Process(target=start_asyncio,args=(sub_page,file_dir,i+1))
        p.start()

    sub_page = pages[end:]
    p = multiprocessing.Process(target=start_asyncio, args=(sub_page, file_dir, process_num))
    p.start()






if __name__ == '__main__':
    settings = {
        "type": "anime",
        "size": "2560x1080",
        "path": "d:/dowload",
        "multi_process": 4
    }

    start_mltp(settings)
    # start_async(settings)
    # mult_num = settings['multi_process']
    # for i in range(mult_num):
    #     p = multiprocessing.Process(target=start_async,args=(settings,))