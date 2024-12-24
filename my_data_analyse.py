import datetime

# 獲取當前車輛信息
def get_bus_on_road(response, time):
    bus_on_road = []
    route_info = response['data']['routeInfo']
    for bus_station in route_info:
        # 當前車站的有幾輛車
        bus_at_station = bus_station['busInfo']
        # 如果不爲空
        if bus_at_station != []:
            # 將車牌信息存入列表
            for bus in bus_at_station:
                # 时间、車站編號、靠站狀態、車牌
                bus_on_road.append([time, bus_station['staCode'], bus['status'], bus['busPlate']]) 

    return bus_on_road



# 获取该线路有哪些站点
def get_station_list(response):
   return [i['staCode'] for i in response['data']['routeInfo']]


# 时间转换
# 将 2024-11-09_00-34-59 转换成 unix 时间戳（秒）
def time_convert_to_seconds(time: str):
    time = time.replace('_', ' ')
    time = time.replace('-', ':')
    time = time.replace(' ', '-')
    time = time.replace(':', '-')
    time = time.split('-')
    time = [int(i) for i in time]
    return int(datetime.datetime(time[0], time[1], time[2], time[3], time[4], time[5]).timestamp())



def seconds_convert_to_time(seconds: int):
    return datetime.datetime.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')







'''
输入: bigdata, station_list
bigdata 样例:
[['2024-11-09_00-09-55', 'M139/2', '0', 'AA2705'],
 ['2024-11-09_00-09-55', 'M3/1', '1', 'AA7192'],
 ['2024-11-09_00-10-02', 'M139/2', '0', 'AA2705'],
 ['2024-11-09_00-10-02', 'M3/1', '1', 'AA7192'],
 ['2024-11-26_14-12-32', 'M3/1', '1', 'AA7010'],
 ...]
该路线近500条信息(车辆多要设置大一点的值)

station_list 样例:
['M1/5', 'M225', 'M229', 'M12', 'M31', 'M16/1', 'M111', 'M112', 'M127', 'M125', 'M136/1', 'M139/2', 'M184', 'M188', 'M203/1', 'M3/1']

返回len(station_list)-1个列表, 每个列表中的元素代表收集的该站点到下一站点的时间
'''
def calculate_time_between_station(big_data, station_list):
    # 获取big_data中的车牌信息再根据0,1切换、且同车牌、相隔站点

    # 过滤车牌
    bus_plate_set = list(set([i[3] for i in big_data]))
    print(f"big_data中的车牌信息:{bus_plate_set}")

    # 结果列表：返回站点间的耗时
    estimated_time = [[] for i in range(len(station_list)-1)]

    for bus in bus_plate_set:
        # 获取单辆车的信息
        single_bus_data = [i for i in big_data if i[3] == bus]

        # 到站、离站的改变
        change_point_list = []
        
        for index in range(len(single_bus_data)-1):
            # 如果是同一辆车，且相邻两个站点

            
            if single_bus_data[index][2] != single_bus_data[index+1][2]:
                change_point_list.append(single_bus_data[index])
                change_point_list.append(single_bus_data[index+1])


        for i in range(len(change_point_list)-3):
            # 检测连续的4行是否符合1001的特征 第二个0代表离开A站 第四个1代表到达B站
            if change_point_list[i][2] and change_point_list[i+3][2] == '1':
                if change_point_list[i+1][2] and change_point_list[i+2][2] == '0':
                    # 检测A、B站是否是相邻站点
                    if station_list.index(change_point_list[i+1][1])+1 == station_list.index(change_point_list[i+3][1]):
                        # 计算时间
                        time_consumed = time_convert_to_seconds(change_point_list[i+3][0])-time_convert_to_seconds(change_point_list[i+1][0])
                        
                        # # 记录时间(到达B站的时间戳)
                        # estimated_time[station_list.index(change_point_list[i+1][1])].append((change_point_list[i+3][0], time_consumed))
                        
                        # 记录时间（离开A站的时间戳）
                        estimated_time[station_list.index(change_point_list[i+1][1])].append((change_point_list[i+1][0], bus, time_consumed))
                        
                        # 不输出所有的时间
                        # estimated_time[station_list.index(change_point_list[i+1][1])].append(time_consumed)
                        
                        # print(f"车牌:{bus} 在{change_point_list[i+1][1]}到{change_point_list[i+3][1]}的时间为{time_consumed}秒") 
                
    # 离开A站的时间，车牌号，持续多久时间到下一站
    return estimated_time




