from datetime import timedelta

import pandas as pd

from Preprocessing.read_file_to_list import get_emotion_data_list

'''
计算表格中的情感值列，加权求平均情感值
'''


def sum_emotion(data_list, time_sum):
    if not data_list:
        return 0

    start_time = data_list[0][0]
    end_time = start_time + timedelta(hours=time_sum)

    emotion_sum = 0
    count = 0

    for entry in data_list:
        publish_time, emotion_value = entry
        if start_time <= publish_time <= end_time:
            emotion_value = Emotional_value_adjustment(emotion_value)
            emotion_sum += emotion_value
            count += 1

    if count == 0:
        return 0
    else:
        return emotion_sum / count


def Emotional_value_adjustment(emotion_value):
    '''
    加权函数
    :param emotion_value:
    :return:
    '''
    emotion_value -= 0.5
    if emotion_value > 0:
        emotion_value *= 0.7
    else:
        emotion_value *= 1
    return emotion_value

if __name__ == '__main__':
    filename = '单亲妈妈网恋遇假军官被骗15万'  # 请替换成你文件的实际路径
    filename = r'..\data\test\comment_sum\\' + filename + '.xlsx'
    emotion_data_list=get_emotion_data_list(filename)
    U= sum_emotion(emotion_data_list,5)
    print(f"计算结果为: {U}")
