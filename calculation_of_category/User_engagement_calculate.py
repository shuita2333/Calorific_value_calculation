import pandas as pd
from datetime import datetime, timedelta
import math

from Preprocessing.read_file_to_list import get_user_data_list

'''
用户参与度计算
'''



def count_messages_in_timeframe(data_list, log_total, log_maxH, par_U_dc, par_U_c, time_subsection, time_sum):
    '''
    用户参与度计算
    :param data_list: 评论数据列表，每个元素是一个字典，包含'发布时间'键
    :param log_total: 总评论数计算公式log值
    :param log_maxH: 最多小时评论数计算公式log值
    :param par_U_dc: 总评论数参数
    :param par_U_c: 最多小时评论数参数
    :param time_subsection: 时间段划分
    :param time_sum: 总时间长度（小时）
    :return: U 用户参与度
    '''
    print("用户参与度计算中。。。")

    # 检查列表是否为空
    if not data_list:
        print("数据列表为空")
        return -1

    # 检查列表中的第一个元素是否含有'发布时间'键
    if '发布时间' not in data_list[0]:
        print("数据列表中的元素没有包含'发布时间'键")
        return -1

    # 对列表进行排序
    data_list.sort(key=lambda x: x['发布时间'])

    # 获取开始时间和结束时间
    start_time = data_list[0]['发布时间']
    end_time = start_time + timedelta(hours=time_sum)

    # 过滤出在开始时间和结束时间之间的数据
    filtered_data_list = [record for record in data_list if start_time <= record['发布时间'] < end_time]

    # 计算总消息数量
    total_message_count = len(filtered_data_list)

    # 如果没有消息，则直接返回
    if total_message_count == 0:
        print("在指定时间内没有消息")
        return 0, 0, 0, 0

    # 将数据按时间段进行分组
    time_groups = {}
    for record in filtered_data_list:
        time_key = record['发布时间'] - timedelta(minutes=record['发布时间'].minute % (time_subsection * 12),
                                                  seconds=record['发布时间'].second,
                                                  microseconds=record['发布时间'].microsecond)
        if time_key not in time_groups:
            time_groups[time_key] = 0
        time_groups[time_key] += 1

    time_keys = list(time_groups.keys())
    last_period_key = time_keys[-1]
    max_count = max(time_groups.values())
    max_period_key = max(time_groups, key=time_groups.get)
    time_interval = time_keys.index(last_period_key) - time_keys.index(max_period_key)
    if time_interval > 0:  # max_count 不在最后一个时间段
        max_count = max_count / (time_interval ** 2)
        if max_count<1:
            max_count = 1


    if len(time_groups) >= 2:
        second_last_period_count = time_groups[time_keys[-2]]

        if second_last_period_count > 0:
            increase_count = time_groups[last_period_key] - second_last_period_count
            if increase_count > 1:
                increase_count = math.log(increase_count, 10)
        if increase_count <= 0:
            increase_count = 0
        increase_count += 1
    else:
        increase_count = 1


    U = (par_U_c * math.log(total_message_count, log_total) + par_U_dc * math.log(max_count, log_maxH)) * increase_count

    return U, increase_count, total_message_count, max_count


if __name__ == '__main__':
    filename = '00后开始在对联上整活了'  # 请替换成你文件的实际路径
    filename = r'..\data\test\comment_sum\\' + filename + '.xlsx'

    # 读取数据
    data_list = get_user_data_list(filename)

    # 计算用户参与度
    U, increase_count, total_message_count, max_count = count_messages_in_timeframe(data_list, 10, 10, 1, 1, 5, 5)
    print(f"计算结果为: {U}")
