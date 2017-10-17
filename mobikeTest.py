import time
import sqlite3
import json

import mobike as mb
# import readArcGISJson as raj

s_time = time.time()
# file_path = '绿道.json'
# # csv_file_name = '绿道result.csv'
# folder_path = "GreenwayJson/"
# gw_name = "总绿道"
# date = "201710161700"
# lng_lat_list = raj.read_arc_json(file_path)
# err_list = [0]
# counter = 0
# all_result = []
# while counter <= 10 and len(lng_lat_list) != 0:
#     r_obj = mb.mobike_requests_in_is(lng_lat_list, mb.default_headers, mb.default_data, city_code='027',
#                                      csv_file_name=csv_file_name)
#     counter += 1
#     err_list = r_obj['err']
#     result = r_obj['result']
#     all_result = all_result + result
#     print(len(err_list))
#     lng_lat_list = err_list
# with open("data.json", "w", encoding="UTF-8") as f_dump:
#     s_dump = json.dump(all_result, f_dump, ensure_ascii=False)
folder_path = "GreenwayJson/"
greenway1 = ["东湖绿道", "金银湖绿道", "沙湖绿道"]
greenway2 = ["后官湖绿道", "江夏环山绿道", "墨水湖绿道"]
greenway2 = ["月湖知音湖", "张公堤绿道"]
greenway_list=greenway1
start_time="2017-10-17 12:00:00"
end_time="2017-10-17 15:00:00"
# mb.mobike_requests_db_retry(lng_lat_list, gw_name, date, mb.default_headers, mb.default_data, table_name="MOBIKE",
#                             city_code='027', max_iteration=5)
mb.timing_start_spy(greenway_list, folder_path, start_time, end_time, d_minute=30)

e_time = time.time()
print('Total time:')
print(e_time - s_time)
