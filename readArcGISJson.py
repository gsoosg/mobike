import json


def read_arc_json(file_path):
    f = open(file_path, encoding='utf-8')
    feature_class = json.load(f)
    features = feature_class['features']
    lat_long_list = []
    for feature in features:
        lat = feature['attributes']['LAT']
        lng = feature['attributes']['LNG']
        lat_long_list.append([lng, lat])
    return lat_long_list
