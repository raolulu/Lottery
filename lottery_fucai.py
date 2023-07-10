#!/usr/bin/python
# coding=utf-8
import requests, bs4
import random
import os, time
import operator
from itertools import combinations, permutations
import torch
proxies = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}

class DoubleColorBall(object):
    def __init__(self):
        self.balls = {}
        self.baseUrl = 'http://tubiao.zhcw.com/tubiao/ssqNew/ssqJsp/ssqZongHeFengBuTuAsc.jsp'
        self.dataFile = './balls_data3.txt'
        self.allBalls = []

    def getHtml(self, url):
        headers = {
            'Referer': 'http://tubiao.zhcw.com/tubiao/ssqNew/ssqInc/ssqZongHeFengBuTuAsckj_year=2016.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.session = requests.Session()
        response = self.session.get(url, headers=headers, proxies=proxies)
        return response.text

    def getBall(self):
        if os.path.exists(self.dataFile):
            os.remove(self.dataFile)
        for year in range(2003, 2024):
            url = self.baseUrl + '?kj_year=%s' % (year,)
            print(url)
            html = self.getHtml(url)
            self.bs = bs4.BeautifulSoup(html, 'html.parser')
            if self.bs:
                data = self.bs.find_all(class_='hgt')
                self.parseBall(data)

    def parseBall(self, data):
        self.balls = {}
        for row in data:
            if not isinstance(row, bs4.element.Tag):
                continue
            center = row.find(class_="qh7").string.strip()
            print(center)
            if center.startswith("模拟"):
                break
            redBalls = row.find_all(class_="redqiu")
            blueBall = row.find(class_="blueqiu3").string.strip()
            self.balls[center] = [r.string for r in redBalls] + [blueBall]
            print(self.balls[center])

        self.saveBall(self.balls)

    def saveBall(self, data):
        with open(self.dataFile, 'a+') as f:
            for r in sorted(data, reverse=False):  #降序
            # for r in sorted(data, reverse=True):  #升序
                f.write(str(r) + ' ' + ' '.join(data[r]) + '\n')
                self.allBalls.append(' '.join(data[r]))
        f.close()

    def getBallList(self):
        return self.allBalls

def create_red_nums(select_num):
    list = []
    for i in range(1, 34):
        if i == select_num:
            continue
        list.append(i)
    return list


def create_blue_nums(select_num):
    list = []
    for i in range(1, 17):
        if i == select_num:
            continue
        list.append(i)
    return list


# 从小到大
def sort_fusion_num(red_list, blue_list):
    red_list.sort()
    blue_list.sort()
    list_str = []
    for i in red_list:
        list_str.append(str(i))
    for i in blue_list:
        list_str.append(str(i))
    return " ".join(list_str)

def create_lottery_num(list_data):
    red_list = create_red_nums(0)
    blue_list = create_blue_nums(0)
    select_num = sort_fusion_num(random.sample(red_list, 6), random.sample(blue_list, 1))
    for i in list_data:
        if i == select_num:
            return create_lottery_num(list_data)
    return select_num

if __name__ == '__main__':
    ball = DoubleColorBall()
    ball.getBall()
    print(ball.getBallList())
    print(len(ball.getBallList()))
    select_num = create_lottery_num(ball.getBallList())
    print(select_num)
