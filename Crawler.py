import hashlib
import urllib.parse
import datetime
import os
import requests
from my_utils import *
from my_constant import *
import time
import json

test_bus_info = [
     ['21A', [0, 1]],
     ['25B', [0, 1]],
     ['25BS', [0]],
     ['26A', [0, 1]],
     ['50', [0]],
     ['51A', [0, 1]],
     ['52', [0]],
     ['55', [0]],
     ['56', [0]],
     ['MT4', [0, 1]],
     ['N3', [0]],
     ['N6', [0]]
]



for route_name, dirs in test_bus_info:

    for dir in dirs:

        # 爬蟲獲取數據
        response = get_data_from_web(route_name, dir)
        
        response = response.json()
        print("==============================================")

        print(f"Route: {route_name}, dir: {dir}, Status: {is_off_work_bus(response)}")

        if not is_off_work_bus(response):
            # 获取当前时间
            now = datetime.datetime.now()
            # 生成文件名  '2023-01-29_09-03-30.txt'
            file_name = f'record/{route_name}/{dir}/' + now.strftime("%Y-%m-%d_%H-%M-%S") + '.txt'
    
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
            with open(file_name, 'w') as f:
                f.write(json.dumps(response))
    
            print(f"file_name: {file_name} saved.")

