import requests

url = 'http://c.easygo.qq.com/api/egc/heatmapdata?lng_min=114.35683&lat_max=30.52907&lng_max=114.36488&lat_min=30.51998&level=16&city=%E6%AD%A6%E6%B1%89&lat=undefined&lng=undefined&_token= HTTP/1.1'
headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Mobile/14D27 MicroMessenger/6.5.18 NetType/WIFI Language/en',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'http://c.easygo.qq.com/eg_toc/map.html?origin=&code=01304trk1SjdBj0bxdqk1Waprk104tr8&state=1',
            'Cookie': 'php_session=eyJpdiI6InZPXC9zUjhKTVdoVVRVcDdGeUpadFJBPT0iLCJ2YWx1ZSI6IlNMRlhYMWZWTENaNm9VbDZhcnR3ZzJjXC9Fc1J5SHU4UXdGNkVhV1dnQ00zSHdEVVJnZHB1cXEydU9IUHVPRzA2cEdMVk5TcnRFSWJNNDdSelFhaHBmdz09IiwibWFjIjoiZWFhNDVmZmYyZmRkZjkyZDE5NGFmODQ0MGQzZTg1ZTAyODdlYTBiMWY5MGQwNjc4MjAyODljODRiOGU1YmYxZiJ9; pgv_pvid=3539729131; pgv_pvi=791811072; o_cookie=844402373; pac_uid=0_91d55471ac33f; sd_cookie_crttime=1499703880317; sd_userid=28271499703880317; eas_sid=Z1w419p4M6R8D8K4U2r7C0m1n8; 3g_guest_id=-8903775221744369664; pt2gguin=o0844402373; ptcz=6bf7b02bbdd5380de430274d3b4b7f523f7067e6e757c3e65436db13496aebf0; tvfe_boss_uuid=ec0e6954ae67c8fc; pvid=471930335; RK=jPUe+O33Qy',
            'Connection': 'keep-alive',
'Host': 'c.easygo.qq.com',
'Accept-Encoding': 'gzip, deflate',
'Accept': 'application/json',
'Accept-Language': 'zh-cn',
'X-Requested-With': 'XMLHttpRequest'



}
r = requests.post(url, headers=headers)
result_mobike = r.json()['object']