import hashlib
import urllib.parse
import datetime
import os
import requests

def generate_key(e, t=None):
    n = ""
    
    if t:
        n = '&'.join(f"{key}={value}" for key, value in t.items())
    else:
        n = e.split("?")[1] if '?' in e else ""
    
    # 创建 MD5 哈希对象
    md5 = hashlib.md5()

    # 更新哈希对象
    md5.update(n.encode('utf-8'))

    # 获取十六进制的哈希值
    hash_value = md5.hexdigest()
    
    # 获取当前时间并格式化
    o = datetime.datetime.now().strftime("%Y%m%d%H%M")
    
    
    # print(hash_value)
    # print(o)

    # 插入时间字符串
    hash_value_list = list(hash_value)
    hash_value_list.insert(24, o[8:])  # MM
    hash_value_list.insert(12, o[4:8])  # DDHH
    hash_value_list.insert(4, o[0:4])   # YYYY
    
    return ''.join(hash_value_list)

# # 示例用法
# e = "/ddbus/common/keyPoi/category"
# # t = {"lang": 'pt', "device": 'web', "busPage": 1}
# t = {
#     'action': 'dy',
#     'routeName': '37',
#     'dir': '0',
#     'lang': 'pt',
#     'routeType': '2',
#     'device': 'web',
# }

# result = generate_key(e, t)
# print(result)

# 爬蟲獲取數據
def get_data_from_web(route_name, dir):
    data = {
        'action': 'dy',
        'routeName': route_name,
        'dir': dir,
        'lang': 'pt',
        'routeType': '2',
        'device': 'web',
    }
        
    token = generate_key('/ddbus/common/keyPoi/category', data)
        
    headers = {
        # 'Referer': 'https://bis.dsat.gov.mo:37812/macauweb/routeLine.html?routeName=39&direction=0&language=pt&ver=3.6.8&routeType=2',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'token': token,
    }

    response = requests.post('https://bis.dsat.gov.mo:37812/macauweb/routestation/bus', headers=headers, data=data)

    return response


# 巴士是否在營業時間
def is_off_work_bus(response):
    route_info = response['data']['routeInfo']
    for bus_station in route_info:
        # 如果 busInfo 裏面有信息, 説明該巴士綫路在運營
        if bus_station['busInfo'] != []:
            return False
            
    return True

