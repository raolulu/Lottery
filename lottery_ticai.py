#!/usr/bin/python
# coding=utf-8

import requests
import lotteryInfo as myInfo
import random

proxies = {'http': 'http://localhost:10809', 'https': 'http://localhost:10809'}
# 23077 size = 2443
size = 1000000000
lotteryDrawNum = 'lotteryDrawNum'
lotteryDrawResult = 'lotteryDrawResult'
lotteryUnsortDrawresult = 'lotteryUnsortDrawresult'
lotteryDrawTime = "lotteryDrawTime"


def get_data():
    url = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=" + str(
        size) + "&isVerify=1&pageNo="
    response = requests.get(url, proxies=proxies)
    print(response.status_code)
    print(response.reason)
    print(response.apparent_encoding)
    # print(response.json())
    json_str = response.json()
    jsonList = json_str['value']['list']
    list = []
    for i in jsonList:
        testInfo = myInfo.LotteryInfo(i[lotteryDrawNum], i[lotteryDrawResult], i[lotteryUnsortDrawresult],
                                      i[lotteryDrawTime])
        list.append(testInfo)
        print("num = {0}, result = {1}, unsortResult = {2}, time = {3}".format(testInfo.getLotteryDrawNum(),
                                                                               testInfo.getLotteryDrawResult(),
                                                                               testInfo.lotteryUnsortDrawresult,
                                                                               testInfo.getLotteryDrawTime()))
    return list


def create_red_nums(select_num):
    list = []
    for i in range(1, 36):
        if i == select_num:
            continue
        list.append(i)
    return list


def create_blue_nums(select_num):
    list = []
    for i in range(1, 13):
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


from typing import List

Vector = List[myInfo.LotteryInfo]


def create_lottery_num(list_data: Vector):
    red_list = create_red_nums(0)
    blue_list = create_blue_nums(0)
    select_num = sort_fusion_num(random.sample(red_list, 5), random.sample(blue_list, 2))
    for i in list_data:
        if i.lotteryDrawResult == select_num:
            return create_lottery_num(list_data)
    return select_num


if __name__ == "__main__":
    listData = get_data()
    print("all history num size = {}".format(len(listData)))
    selectList = [] * 2
    while len(selectList) < 2:
        select_num = create_lottery_num(listData)
        if select_num in selectList:
            continue
        selectList.append(select_num)
    print(selectList)
