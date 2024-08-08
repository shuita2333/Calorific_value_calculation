import pandas as pd
import os
from datetime import timedelta

from Preprocessing.read_file_to_list import get_news_data_list

'''
新闻关注度计算
'''


# def count_exceeding_messages(folder_path, par_N,time_subsection,time_sum):
#     '''
#     媒体关注度计算
#     :param folder_path: 评论文件名称
#     :param par_N: 媒体关注度除法分母参数（不能为零）
#     :return: N 媒体关注度
#     '''
#     print("媒体关注度计算中。。。")
#     # folder_path = r'data\test\comment\\' + folder_path
#     # 设定初始计数为零
#     exceeding_files_count = 0
#     # # 给定评论量加和比例
#     # sum_ratio = 1 / (time_sum / time_subsection)
#
#     # 遍历文件夹下的所有Excel文件
#     for file_name in os.listdir(folder_path):
#         if file_name.endswith('.xlsx'):
#             file_path = os.path.join(folder_path, file_name)  # 获取文件完整路径
#
#             try:
#                 # 读取Excel文件
#                 df = pd.read_excel(file_path, engine='openpyxl')
#             except:
#                 return -1
#
#             # 检查是否有'发布时间'列并转换为datetime
#             if '发布时间' not in df.columns:
#                 print(f"The column '发布时间' does not exist in {file_name}. Skipping this file.")
#                 continue
#
#             df['发布时间'] = pd.to_datetime(df['发布时间'], format='%a %b %d %H:%M:%S %z %Y')
#             df.sort_values('发布时间', inplace=True)  # 确保时间顺序
#
#             # 获取最后一时间段的消息
#             # start_time = df.iloc[0]['发布时间']+ timedelta(hours=time_sum-time_sum/time_subsection)
#             start_time = df.iloc[0]['发布时间']
#             end_time = start_time + timedelta(hours=time_sum)
#             data_5_hours = df[(df['发布时间'] >= start_time) & (df['发布时间'] < end_time)]
#
#             # 检查总消息数是否超过100条
#             if len(data_5_hours) > 100:
#                 exceeding_files_count += 1
#                 continue  # 当前文件已满足条件，无需进一步检查
#
#     N = exceeding_files_count / par_N + 1
#     return N

def count_exceeding_messages(data_dict, par_N, time_sum):
    '''
    根据提供的文件数据计算媒体关注度
    :param data_dict: 包含每个文件数据列表的字典
    :param par_N: 媒体关注度除法分母参数（不能为零）
    :param time_sum: 总时间长度（小时）
    :return: N 媒体关注度
    '''
    print('新闻关注度计算中。。。')
    exceeding_files_count = 0

    for file_name, data_list in data_dict.items():
        # 将数据列表转换回DataFrame来方便处理
        df = pd.DataFrame(data_list)
        df.sort_values('发布时间', inplace=True)

        if not df.empty:
            start_time = df.iloc[0]['发布时间']
            end_time = start_time + timedelta(hours=time_sum)
            filtered_df = df[(df['发布时间'] >= start_time) & (df['发布时间'] < end_time)]

            if len(filtered_df) > 100:
                exceeding_files_count += 1

    N = exceeding_files_count / par_N + 1
    return N


if __name__ == '__main__':
    folder_path = r'00后把新年的颜色玩明白了'  # 替换成你的文件夹路径
    folder_path = r'..\data\test\comment\\' + folder_path
    processed_data = get_news_data_list(folder_path)
    total_exceeding_files = count_exceeding_messages(processed_data,10,5)
    print(f"Total files with messages exceeding the threshold: {total_exceeding_files}")
