import mobike as mb

start = [114.356, 30.530]
end = [114.387, 30.553]
# #
# start = [114.356, 30.543]
# end = [114.356, 30.543]
# 西北角114.348051,30.60365；西南角114.348913,30.517075；东北角114.465046,30.604396；东南角114.475969,30.511599
start = [114.348, 30.511]
end = [114.476, 30.605]
mb.mobike_rect2(start[0], start[1], end[0], end[1], offset=0.001, city_code='027', csv_file_name='donghulvdao_2.csv')
