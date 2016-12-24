# -*- coding: utf-8 -*-

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
from DEF_DATA import data as data_mod
from Utils.SQL_API import SQL_API as sql
from pymysql import err as sqlerr
from lxml import html
import time
import datetime

# import sqlite3 as sql

class Networkerror(Exception):
    def __init__(self, arg):
        self.args = arg

class DBerror(Exception):
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
        return "未知"


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
        return "未知"

def get_finish_state(i):
    # input a num
    # output finish state
    if i == 1:
        return '连载中'
    elif i == 2:
        return '完结'
    elif i == 0:
        return '未开播'
    else:
        return '未知'


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


def save_data_to_file(datalist,urllist):
    """
    THis is function for saving data to file

    :param datalist: LIST which elements is a DICT from json pkg
    :param urllist: LIST which elements is url strings
    :return:
    :output: data.d (file contain all data) url.d　(file contain all urls)
    """
    try:
        f1 = open('data.d','w+',encoding='utf-8')
        f1.write('season_id||title||cover||favorites||pub_time||update_time||is_finish||country||type||week||url\n')
        for data in datalist:
            line_data = []
            line_data.append(data['season_id'])
            line_data.append(data['title'])
            line_data.append(str(data['favorites']))
            pub_time = time.strftime('%Y-%m-%d',time.localtime(data['pub_time'])) # use localtime for reading
            line_data.append(pub_time + ',' + str(data['pub_time']))
            update_time = time.strftime('%Y-%m-%d',time.localtime(data['update_time']))
            line_data.append(update_time + ',' + str(data['update_time']))
            line_data.append(data['week'])
            line_data.append(get_country_name(data['country']))
            line_data.append(get_type_name(data['type']))
            line_data.append(get_finish_state(data['is_finish']))
            line_data.append(data['url'])
            line_data.append(data['cover'])
            line_str = "||".join(line_data)
            f1.write(line_str+'\n')
        f1.close()

        f2 = open('url.d','w+')
        for url in urllist:
            f2.write(url + '\n')
    except Exception as e:
        print(str(x) for x in e)
        return 0
    return 1

def save_data_to_sql(db,datalist):
    """
    This function can be  used for save all data in datalist to database
    :type db: sql
    :param db: sql
    :param datalist:
    :return:
    """

    count = 0
    for d_data in datalist:
        count += 1
        data= data_mod()
        try:
            data.id = int(d_data['season_id'])
            data.name = d_data['title'].replace("\'"," ")
            data.favorite = d_data['favorites']

            # pub_time = time.localtime(d_data['pub_time'])
            # year = time.strftime('%Y',pub_time)
            # month = time.strftime('%m',pub_time)

            ## time trans
            pub_time = datetime.datetime(1970,1,1) + datetime.timedelta(seconds=d_data['pub_time']+28800)
            year = pub_time.year
            month = pub_time.month
            data.year = int(year)
            data.season = int(month)
            data.pubtime = d_data['pub_time']
            data.status = d_data['is_finish']
            data.updatetime = d_data['update_time']
            try:
                data.week = int(d_data['week'])
            except KeyError as e:
                data.week = -2
            data.country = d_data['country']
            data.types = d_data['type']
            data.url = d_data['url']
            data.cover = d_data['cover']
        except Exception as e:
            print(d_data)
            print(e)

        try:
            db.save_anime_data(data)
        except sqlerr.Error as e:
            print("[-]ERROR OCCUR IN SAVE COUNT %d DATA" % count)
            print("[--]ERROR CODE IS :" + str(e))
            print("[--]ERROR DATA IS :" + str(data))





def main():
    tp = tps()
    TYPE = [tp.TYPE_TV, tp.TYPE_THEME, tp.TYPE_OVA, tp.TYPE_OTHER]
    COUNTRY = [tp.DIS_CHINA, tp.DIS_JAPAN, tp.DIS_AMARECAN, tp.DIS_OTHER]
    db = sql('bilibili')

    anime_url_list = []
    for t in TYPE:
        for c in COUNTRY:
            datalist = []
            # get pages info
            print("[+]正在提取的数据类型为%s-%s:" % (get_type_name(t),get_country_name(c)))
            page = 1
            url = "http://bangumi.bilibili.com/web_api/season/index?page=%d&page_size=20&version=%d" \
                  "&is_finish=0&start_year=&quarter=0&tag_id=&index_type=1&index_sort=0&area=%d" % (page, t, c)
            process = Get_list_data(url)
            pages = int(process.pages)
            print ('[+--]总页面数为:%d' % pages)
            if not pages:
                continue
            # collect all datas in type and country
            for page in range(1, pages + 1):
                print('[+--]正在提取第 %d 页...' % page)
                if page != 1:
                    url = "http://bangumi.bilibili.com/web_api/season/index?page=%d&page_size=20&version=%d" \
                          "&is_finish=0&start_year=&quarter=0&tag_id=&index_type=1&index_sort=0&area=%d" % (
                              page, t, c)
                    del process
                    process = Get_list_data(url)

                # Save url to url list
                anime_url_list.extend(process.get_comic_url_list())
                details = process.get_details()
                add_info_to_detail(details, c, t)
                datalist.extend(details)
                time.sleep(1)
            print("[+--]存储数据...：%s - %s" % (get_country_name(c), get_type_name(t)))
            save_data_to_sql(db, datalist)


    # save_data_to_file(datalist,anime_url_list)




    # SAVE datalist and commic_url_list
    # db = sql('bilibili')
    # try:
    #     db.init_db()
    # except Exception as e:
    #     print (str(x) for x in e)
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
    # db = sql('bilibili')
    # data1 = {'country': 2, 'season_status': 2, 'cover': 'http://i0.hdslb.com/bfs/bangumi/fcfd760465cf27b532b5b304352d597262f2fffa.jpg', 'update_time': 1403783691, 'title': '哆啦A梦 春之章', 'is_finish': 2, 'favorites': 15449, 'url': 'http://bangumi.bilibili.com/anime/2457', 'total_count': 6, 'pub_time': 291916800, 'newest_ep_index': '85年', 'season_id': '2457', 'type': 1}
    # data2 = {'country': 2, 'season_status': 2, 'cover': 'http://i0.hdslb.com/bfs/bangumi/67994e27b82d40b88b025e4bcaefb3ba0a199b3f.jpg', 'update_time': 1369807086, 'title': '棒球大联盟 第三季', 'is_finish': 2, 'favorites': 1309, 'url': 'http://bangumi.bilibili.com/anime/1029', 'total_count': 26, 'pub_time': 1136563200, 'newest_ep_index': '26', 'season_id': '1029', 'type': 1}
    # datalist = [data1,data2]
    # save_data_to_sql(db,datalist)
    pass
