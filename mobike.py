# coding: utf-8
import pickle as pickle

import math
import sqlite3

import requests
from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import csv
import time
import datetime as dt

import readArcGISJson as raj

url = 'https://mwx.mobike.com/mobike-api/rent/nearbyBikesInfo.do'
default_headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, '
                  'like Gecko) Mobile/14E304 MicroMessenger/6.5.7 NetType/WIFI Language/zh_CN',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://servicewechat.com/wx80f809371ae33eda/48/page-frame.html ',
}
default_data = {
    'longitude': '',
    'latitude': '',
    'citycode': '',
}


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


def mobike_point(lng_lat_list, city_code='027', csv_file_name='mobike_result.csv'):
    s_time = time.time()
    csv_file = open(csv_file_name, 'w')
    writer = csv.writer(csv_file)
    # 写入columns_name
    col_names = ["distId", "distX", "distY", "distNum", "distance", "bikeIds", "biketype", "type", "boundary"]
    writer.writerow(col_names)
    result_mobike = mobike(lng_lat_list, city_code)
    result_csv = reformat_mobike_data(result_mobike, col_names)
    writer.writerows(result_csv)
    e_time = time.time()
    print(e_time - s_time)
    return


def mobike_requests(lng_lat_list, headers, data, city_code='027', csv_file_name='mobike_result.csv'):
    s_time = time.time()
    csv_file = open(csv_file_name, 'w')
    writer = csv.writer(csv_file)
    # 写入columns_name
    col_names = ["distId", "distX", "distY", "distNum", "distance", "bikeIds", "biketype", "type", "boundary"]
    writer.writerow(col_names)
    count = 1
    err_list = []
    for lng_lat in lng_lat_list:
        data['longitude'] = lng_lat[0]
        data['latitude'] = lng_lat[1]
        data['citycode'] = city_code
        try:
            r = requests.post(url, data=data, headers=headers, timeout=0.3)
            result_mobike = r.json()['object']
            result_csv = reformat_mobike_data(result_mobike, col_names)
            writer.writerows(result_csv)
            print(count)
        except:
            time.sleep(0.3)
            print('E' + str(count))
            err_list.append(lng_lat)
        count = count + 1
        time.sleep(0.01)
    e_time = time.time()
    print(e_time - s_time)
    return err_list


def mobike_requests_in_is(lng_lat_list, headers, data, city_code='027', csv_file_name='mobike_result.csv'):
    s_time = time.time()
    # 写入columns_name
    col_names = ["distId", "distX", "distY", "distNum", "distance", "bikeIds", "biketype", "type", "boundary"]
    count = 1
    result = []
    err_list = []

    for lng_lat in lng_lat_list:
        data['longitude'] = lng_lat[0]
        data['latitude'] = lng_lat[1]
        data['citycode'] = city_code
        try:
            r = requests.post(url, data=data, headers=headers, timeout=0.3)
            result_mobike = r.json()['object']
            result.append(result_mobike)
            # result_csv = reformat_mobike_data(result_mobike, col_names)
            # writer.writerows(result_csv)
            print(count)
        except:
            time.sleep(0.3)
            print('E' + str(count))
            err_list.append(lng_lat)
        count = count + 1
        time.sleep(0.01)
    e_time = time.time()
    print(e_time - s_time)
    return {'result': result, 'err': err_list}


def mobike_requests_db_retry(lng_lat_list, gw_name, date, headers, data, table_name="MOBIKE", city_code='027',
                             max_iteration=10):
    s_time = time.time()
    conn = sqlite3.connect('data.db')
    sql_cursor = conn.cursor()
    keys_list = ["distId", "distX", "distY", "distNum", "distance", "bikeIds", "biketype", "type", "boundary", "GWName",
                 "DATE"]
    result = []
    iteration = 0
    while iteration <= max_iteration and len(lng_lat_list) != 0:
        count = 1
        err_list = []
        for lng_lat in lng_lat_list:
            data['longitude'] = lng_lat[0]
            data['latitude'] = lng_lat[1]
            data['citycode'] = city_code
            try:
                r = requests.post(url, data=data, headers=headers, timeout=0.3)
                result_mobike = r.json()['object']
                r_list = insert_mobike_data(sql_cursor, result_mobike, gw_name, date, table_name, keys_list)
                conn.commit()
                result = result + r_list
                print(count)
            except Exception as err:
                print(err.args[0])
                time.sleep(0.3)
                print('E' + str(count))
                err_list.append(lng_lat)
            count = count + 1
            time.sleep(0.01)

        iteration = iteration + 1
        print(len(err_list))
        lng_lat_list = err_list
    e_time = time.time()
    conn.close()
    print(e_time - s_time)
    return result


def insert_mobike_data(sql_cursor, result_mobike, gw_name, date, table_name, keys_list):
    result = []
    for m_obj in result_mobike:
        m_obj["GWName"] = gw_name
        m_obj["DATE"] = date
        insert_str = create_insert(table_name, keys_list)
        value_list = get_value_list(m_obj, keys_list)
        sql_cursor.execute(insert_str, value_list)
        result.append(m_obj)
    return result


def create_insert(table_name, keys_list):
    key_str = ""
    value_str = ""
    for key in keys_list:
        key_str = key_str + key + ", "
        value_str = value_str + "?, "
    key_str = key_str[0:-2]
    value_str = value_str[0:-2]
    sql_str = "INSERT INTO " + table_name + " (" + key_str + ") VALUES (" + value_str + ")"
    return sql_str


def get_value_list(obj, keys_list):
    value_list = []
    for key in keys_list:
        value_list.append(get_value(obj, key))
    return value_list


def get_value(value_obj, key):
    if key in value_obj:
        value = value_obj[key]
        if value is None:
            value = "-9999"
    else:
        value = "-9999"
    return value


def spy_greenway(greenway_list, folder_path, date):
    for gw_name in greenway_list:
        file_path = folder_path + gw_name + ".json"
        lng_lat_list = raj.read_arc_json(file_path)
        mobike_requests_db_retry(lng_lat_list, gw_name, date, default_headers, default_data, table_name="MOBIKE",
                                 city_code='027', max_iteration=5)


def timing_start_spy(greenway_list, folder_path, start_time, end_time, d_minute=30):
    s_time = dt.datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S')
    e_time = dt.datetime.strftime(end_time, '%Y-%m-%d %H:%M:%S')
    d_m = dt.timedelta(minutes=d_minute)
    date_time_list = []
    c_time = s_time
    while c_time <= e_time:
        t_obj = {"dt": c_time, "dts": c_time.strftime("%Y%m%d%H%M")}
        date_time_list.append(t_obj)

    for t_obj in date_time_list:
        datetime_obj = t_obj["dt"]
        datetime_str = t_obj["dts"]
        now_time = dt.datetime.now()
        d_dt = now_time - datetime_obj
        if d_dt.seconds > d_minute * 60:
            continue
        while now_time < datetime_obj:
            time.sleep(60)
            now_time = dt.datetime.now()
        spy_greenway(greenway_list, folder_path, datetime_str)
