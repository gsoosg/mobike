import time

import mobike as mb

s_time = time.time()
folder_path = "GreenwayJson/"
greenway1 = ["东湖绿道", "金银湖绿道", "沙湖绿道"]
greenway2 = ["后官湖绿道", "江夏环山绿道", "墨水湖绿道"]
greenway2 = ["月湖知音湖", "张公堤绿道"]
greenway_list = greenway1
start_time = "2017-10-17 15:04:00"
end_time = "2017-10-17 15:30:00"
mb.timing_start_spy(greenway_list, folder_path, start_time, end_time, d_minute=30)

e_time = time.time()
print('Total time:')
print(e_time - s_time)
