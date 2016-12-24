# encoding: utf-8

"""
@version: v1.0
@author: nyansama
@contact: nyansama@163.com
@software: PyCharm
@file: DEF_DATA.py
@time: 2016/12/19 20:16
"""


class data:
    def __init__(self):
        self.id = -2
        self.name = ""
        self.favorite = -2
        self.year = -2
        self.season = -2
        self.pubtime = -2
        self.status = -2
        self.total_count = -2
        self.updatetime = -2
        self.week = -2
        self.country = -2
        self.types = -2
        self.url = ""
        self.cover = ""

    def __str__(self):
        data_list = []
        data_list.append(str(self.id))
        data_list.append(self.name)
        data_list.append(str(self.favorite))
        data_list.append(str(self.year))
        data_list.append(str(self.season))
        data_list.append(str(self.pubtime))
        data_list.append(str(self.status))
        data_list.append(str(self.total_count))
        data_list.append(str(self.updatetime))
        data_list.append(str(self.week))
        data_list.append(str(self.country))
        data_list.append(str(self.types))
        data_list.append(self.url)
        data_list.append(self.cover)
        return ",".join(data_list)


class types:
    def __init__(self):
        # TYPE NUM DEFINE
        # global TYPE_TV, TYPE_ALL, TYPE_OVA, TYPE_THEME, TYPE_ORTHER
        self.TYPE_ALL = 0
        self.TYPE_TV = 1
        self.TYPE_OVA = 2
        self.TYPE_THEME = 3
        self.TYPE_OTHER = 4

        # AREA DEFINE
        # global DIS_CHINA, DIS_JAPAN, DIS_AMARECAN, DIS_ORTHER
        self.DIS_CHINA = 1
        self.DIS_JAPAN = 2
        self.DIS_AMARECAN = 3
        self.DIS_OTHER = 4

        # SEASON
        # global SPRING, SUMMER, AUTUMN, WINTER
        self.WINTER = 1
        self.SPRING = 2
        self.SUMMER = 3
        self.AUTUMN = 4

        # COMMIC TYPE DEFINE
        # global


