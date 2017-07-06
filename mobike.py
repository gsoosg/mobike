# coding: utf-8
import pickle as pickle

import math
import requests
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import csv
import time


def load_url(url, params, timeout, headers=None):
    return requests.get(url, params=params, timeout=timeout, headers=headers).json()


def merge_dicts(*dict_args):
    # u"可以接收1个或多个字典参数"
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def mobike(location_list, city_code='027'):
    all_mobike = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        url = 'https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do'
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                          'like Gecko) Mobile/14E304 MicroMessenger/6.5.7 NetType/WIFI Language/zh_CN',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx80f809371ae33eda/48/page-frame.html ',
        }
        data = {
            'longitude': '',
            'latitude': '',
            'citycode': city_code,
        }
        future_to_url = {
            executor.submit(load_url, url,
                            merge_dicts(data, {'longitude': i[0]}, {'latitude': i[1]}), 5,
                            headers): url for i in location_list}
        for future in futures.as_completed(future_to_url):
            if future.exception() is not None:
                print(future.exception())
            elif future.done():
                data = future.result()['object']
                all_mobike.extend(data)
    return all_mobike


def num_range(start, end, offset, fix_num=3):
    result_range = []
    tmp_num = start
    math.log10(offset)

    while tmp_num < end:
        result_range.append(tmp_num)
        tmp_num = tmp_num + offset
        tmp_num = round(tmp_num, fix_num)
    result_range.append(end)
    return result_range


def reformat_mobike_data(mobike_data, col_names):
    result = []
    for md in mobike_data:
        tmp_result = []
        for col in col_names:
            if col in md:
                tmp_result.append(md[col])
            else:
                tmp_result.append(None)
        result.append(tmp_result)
    return result


def mobike_rect(start_lng, start_lat, end_lng, end_lat, offset=0.001, city_code='027',
                csv_file_name='mobike_result.csv'):
    lng_range = num_range(start_lng, end_lng, offset)
    lat_range = num_range(start_lat, end_lat, offset)
    csv_file = open(csv_file_name, 'w')
    writer = csv.writer(csv_file)
    # 写入columns_name
    col_names = ["distId", "distX", "distY", "distNum", "distance", "bikeIds", "biketype", "type", "boundary"]
    writer.writerow(col_names)
    for lng in lng_range:
        result_mobike = []
        for lat in lat_range:
            # time.sleep(1)
            location_list = [[lng, lat]]
            tmp_mobike = mobike(location_list, city_code)
            result_mobike += tmp_mobike
            print([lng, lat])
        result_csv = reformat_mobike_data(result_mobike, col_names)
        writer.writerows(result_csv)
    return


def mobike_rect2(start_lng, start_lat, end_lng, end_lat, offset=0.001, city_code='027',
                 csv_file_name='mobike_result.csv'):
    s_time = time.time()
    lng_range = num_range(start_lng, end_lng, offset)
    lat_range = num_range(start_lat, end_lat, offset)
    csv_file = open(csv_file_name, 'w')
    writer = csv.writer(csv_file)
    # 写入columns_name
    col_names = ["distId", "distX", "distY", "distNum", "distance", "bikeIds", "biketype", "type", "boundary"]
    writer.writerow(col_names)
    for lng in lng_range:
        location_list = []
        for lat in lat_range:
            tmp_location = [lng, lat]
            location_list.append(tmp_location)
        result_mobike = mobike(location_list, city_code)
        result_csv = reformat_mobike_data(result_mobike, col_names)
        writer.writerows(result_csv)
        print(lng)
    e_time = time.time()
    print(e_time - s_time)
    return
