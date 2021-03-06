# encoding: utf-8

"""
@version: v1.0
@author: nyansama
@contact: nyansama@163.com
@software: PyCharm
@file: get_ani_list.py
@time: 2016/12/18 22:21
"""
import requests as re
import simplejson as json
from DEF_DATA import types as tps
from Utils.SQL_API import SQL_API as sql
from lxml import html


# import sqlite3 as sql

class Networkerror(Exception):
    def __init__(self, arg):
        self.args = arg


def get_type_name(i):
    # input a num
    # output type name
    if i == 1:
        return 'TV'
    elif i == 2:
        return 'OVA/OAD'
    elif i == 3:
        return '剧场版'
    elif i == 4:
        return '其他'
    else:
        return "ALL"


def get_country_name(i):
    # input a num
    # output country name
    if i == 1:
        return "国产"
    elif i == 2:
        return "日本"
    elif i == 3:
        return "美国"
    elif i == 4:
        return "其他"
    else:
        return "ALL"


def add_info_to_detail(details, c, t):
    # input details LIST contain DICT element
    # modify details with country and type
    for data in details:
        data['country'] = c
        data['type'] = t


class Get_list_data:
    def __init__(self, url):
        self._url = url
        self._pkg = re.get(url).content.decode('utf-8')
        self._data = json.loads(self._pkg, 'utf-8')
        message = self._data['message']
        if self._data['message'] != 'success':
            raise Networkerror("Pkg request Fail!\n")
        self.count = self._data['result']['count']
        self.pages = self._data['result']['pages']

    def is_empty(self):
        if not self.count:
            return 0
        return 1

    def get_comic_url_list(self):
        if not self.is_empty():
            return []
        ulist = []
        for commic in self._data['result']['list']:
            url = commic['url']
            ulist.append(url)

        return ulist

    def get_details(self):
        # output data structure is list contain all dict name data

        datalist = []

        for x in self._data['result']['list']:
            datalist.append(x)
        return datalist
        # data = {}
        # data['id'] = x['season_id']
        # data['cover'] = x['cover']
        # data['like_num'] = x['favorites']
        # data['is_finish'] = x['is_finish']
        # data['newest_index'] = x['newest_ep_index']
        # data['pub_time'] = x['pub_time']
        # data['name'] = x['title']
        # data['updata_time'] = x['update_time']
        # data['week'] = x['week']


# def get_list():
#     url = "http://bangumi.bilibili.com/web_api/season/index?page=3&page_size=20&version=0" \
#           "&is_finish=0&start_year=&quarter=0&tag_id=&index_type=1&index_sort=0"
#     jpkg = re.get(url)
#     data = json.loads(jpkg,'utf-8')

def main():
    tp = tps()
    TYPE = [tp.TYPE_TV, tp.TYPE_THEME, tp.TYPE_OVA, tp.TYPE_OTHER]
    COUNTRY = [tp.DIS_CHINA, tp.DIS_JAPAN, tp.DIS_AMARECAN, tp.DIS_OTHER]

    datalist = []
    anime_url_list = []
    for t in TYPE:
        for c in COUNTRY:
            # get pages info
            page = 1
            url = "http://bangumi.bilibili.com/web_api/season/index?page=%d&page_size=20&version=%d" \
                  "&is_finish=0&start_year=&quarter=0&tag_id=&index_type=1&index_sort=0&area=%d" % (page, t, c)
            process = Get_list_data(url)
            pages = int(process.pages)

            if not pages:
                continue
            # collect all datas in type and country
            for page in range(1, pages + 1):
                if page != 1:
                    url = "http://bangumi.bilibili.com/web_api/season/index?page=%d&page_size=20&version=%d" \
                          "&is_finish=0&start_year=&quarter=0&tag_id=&index_type=1&index_sort=0&area=%d" % (
                              page, t, c)
                    process = Get_list_data(url)

                # Save url to url list
                anime_url_list.extend(process.get_comic_url_list())
                details = process.get_details()
                add_info_to_detail(details, c, t)
                datalist.extend(details)

    # SAVE datalist and commic_url_list
    # db = sql('bilibili')
    # db.cur.execute("SELECT 1")



def get_style():
    # db = sql('bilibili')
    # db.init_types()  # just init types
    url = "http://bangumi.bilibili.com/anime/index"
    page = re.get(url).content
    html_str = page.decode('utf-8')
    tree = html.fromstring(html_str)
    lists = tree.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div/div[6]/div[2]/*")
    for x in lists[1:-1]:
        id = x.xpath('./@data-value')[0]
        name = x.text
        # print (id[0] +':' + name + '\n')
        sql_str = "INSERT INTO types(id,name)VALUES(%d,'%s');" % (int(id), name)
        print(sql_str)
        # db.cur.execute(sql_str)
        # print (sql_str)


if __name__ == '__main__':
    # main()

    # with sql('bilibili') as db:
    #     db.init_table()
    # with sql('bilibili') as db:
    #     try:
    #         db.init_table()
    #     except Exception as e:
    #         pass

    # get_style() # finish
    main()
    pass
