import mobike as mb
import readArcGISJson as raj

start = [114.356, 30.530]
end = [114.387, 30.553]
# #
# start = [114.356, 30.543]
# end = [114.356, 30.543]
# 西北角114.348051,30.60365；西南角114.348913,30.517075；东北角114.465046,30.604396；东南角114.475969,30.511599
# start = [114.348, 30.511]
# end = [114.476, 30.605]
# mb.mobike_rect2(start[0], start[1], end[0], end[1], offset=0.0015, city_code='027', csv_file_name='donghulvdao_4.csv')
file_path = '东湖绿道.json'
csv_file_name = '东湖result。csv'
lng_lat_list = raj.read_arc_json(file_path)
err_list=mb.mobike_requests(lng_lat_list, mb.default_headers, mb.default_data, city_code='027', csv_file_name=csv_file_name)
# mb.mobike_point(lng_lat_list, city_code='027', csv_file_name='mobike_result.csv')
try:
    i = 1
except:
    i = 2
