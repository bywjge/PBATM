from flask import Flask, request, jsonify
import os
import json
from my_data_analyse import *
from my_utils import *
import time

app = Flask(__name__)

@app.route('/bus_info', methods=['GET'])
def get_bus_info():
    route = request.args.get('route')
    direction = request.args.get('direction')
    current_station = request.args.get('station')
    # current_station = 'T309'
    # route = '21A'
    # direction = '0'

    all_txt_file = sorted(os.listdir(f'record/{route}/{direction}/'))
    all_txt_file = [i for i in all_txt_file if i.endswith('txt')]
    print(f"record/{route}/{direction}/ 目录下有 {len(all_txt_file)} 条记录")
    # 取后 1500 条数据
    all_txt_file = all_txt_file[-1500:]
    big_data = []
    for i in range(len(all_txt_file)):
        
        with open(f'record/{route}/{direction}/{all_txt_file[i]}', 'r') as f:
            response = f.read()
            response = json.loads(response)
            bus_on_road = get_bus_on_road(response, all_txt_file[i][:-4])
            # 当前请求有哪些巴士在路上
            # print(bus_on_road)
            big_data.extend(bus_on_road)

    # 车站信息
    with open(f'record/{route}/{direction}/{all_txt_file[-1]}', 'r') as f:
        response = f.read()
        response = json.loads(response)
        station_list = get_station_list(response)
        print(f'车站列表: {station_list}')

    # 估计时长
    estimated_time = calculate_time_between_station(big_data, station_list)
    print(estimated_time)

    import time
    # 当前我在哪个车站等车
    # current_station = 'C671' # 收集的数据有点少，奇怪
    # current_station = 'T309'
    current_station_index = station_list.index(current_station)
    previous_station_index = current_station_index - 1
    # 获取现在的时间
    time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    bus_on_road = get_bus_on_road(get_data_from_web(route, int(direction)).json(), time_now)
    print(f"当前在路上的巴士：{bus_on_road}")


    '''
    bus_on_road =
    [['2024-12-09_20-48-34', 'M170/1', '0', 'AB6210'],
    ['2024-12-09_20-48-34', 'T379', '0', 'AA7741']]
    '''

    result = []
    for item in bus_on_road:
        # 巴士现在所在车站的索引
        bus_station_index_now = station_list.index(item[1])
        # 找出在该站之前的车辆
        if bus_station_index_now <= previous_station_index:
            print(f"当前尚未到 {current_station} 站的车辆：{item}")
            # 筛选出该车牌在big_data中的信息
            bus_info = [i for i in big_data if i[3] == item[3]]
            # 筛选该车牌在当前站的信息
            bus_info = [i for i in bus_info if station_list.index(i[1]) == bus_station_index_now]
            # 筛选在该站点等于1的信息
            bus_info = [i for i in bus_info if i[2] == '1']
            if not bus_info:
                continue

            # TODO:有BUG
            print(f"当前车辆离开 {station_list[bus_station_index_now]} 站的时间: {bus_info[-1]}")

            # 已经行驶的时长
            already_drive_second = time_convert_to_seconds(item[0])-time_convert_to_seconds(bus_info[-1][0])
            print(f"当前车辆离开 {station_list[bus_station_index_now]} 站, 已经行驶 {already_drive_second} 秒")

            # 当前车站到下一个站的持续时长
            current_station_estimated_time = estimated_time[bus_station_index_now]
            # 提取出 时长（秒数）
            current_station_estimated_time_list = [i[2] for i in current_station_estimated_time]

            # print(f"从 {station_list[bus_station_index_now]} 到 {station_list[bus_station_index_now+1]} 历史所需时长：{current_station_estimated_time}")
           
            if len(current_station_estimated_time_list) > 4:
                current_station_estimated_time_list = sorted(current_station_estimated_time_list)[2:-2]
            else:
                current_station_estimated_time_list = sorted(current_station_estimated_time_list)

            # print(f"对时间进行排序并去掉头和尾各两条数据: {current_station_estimated_time_list}")

            # 对 current_station_estimated_time_list 计算平均值
            average_time = round(sum(current_station_estimated_time_list) / len(current_station_estimated_time_list))
            print(f"从 {station_list[bus_station_index_now]} 到 {station_list[bus_station_index_now+1]} 平均所需时长: {average_time} 秒")

            # 将平均所需时长与当前已经行驶时长相减，如果为负数则取0
            predict_time = average_time - already_drive_second
            
            if predict_time < 0:
                predict_time = 0

            print(f"预测还有多久到达: {predict_time}")

            # 统计下一个
            for i in range(bus_station_index_now + 1, current_station_index):

                # 当前车站到下一个站的持续时长
                current_station_estimated_time = estimated_time[i]
                # 提取出 时长（秒数）
                current_station_estimated_time_list = [i[2] for i in current_station_estimated_time]

                print(f"从 {station_list[i]} 到 {station_list[i+1]} 历史所需时长：{current_station_estimated_time}")
                # TODO：需要加判断数据是否大于4条
                current_station_estimated_time_list = sorted(current_station_estimated_time_list)[2:-2]
                # 对 current_station_estimated_time_list 计算平均值
                average_time = round(sum(current_station_estimated_time_list) / len(current_station_estimated_time_list))
                print(f"从 {station_list[i]} 到 {station_list[i+1]} 平均所需时长: {average_time} 秒")
                predict_time += average_time

                # 假设乘客上下车每个站占用25秒 
           
                predict_time += 25

            
            print(f"预测还有多久到达: {predict_time} , 预计到达时间 {seconds_convert_to_time(time_convert_to_seconds(item[0])+predict_time)} ")
            print('--'*30)

            result.append([item[3], predict_time, seconds_convert_to_time(time_convert_to_seconds(item[0])+predict_time)])


    return jsonify(result)

if __name__ == '__main__':
    
    app.run(debug=False, port=8889, host='0.0.0.0')