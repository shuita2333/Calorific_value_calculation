from Preprocessing.read_file_to_list import get_user_data_list, get_news_data_list, get_emotion_data_list
from calculation_of_category.News_number_calculate import count_exceeding_messages
from calculation_of_category.Topic_sensitivity_calculation import classify_string
from calculation_of_category.User_engagement_calculate import count_messages_in_timeframe
import os
import openpyxl
import matplotlib.pyplot as plt
from calculation_of_category.cemotion_read_calculate import sum_emotion

'''
新主函数，使用预处理生成的情感数据进行分析 
'''

time_subsection = 20  # 时间间隔数
time_num = 1  # 想要预测显示的时长间隔长度（需要是time_sume的整倍数）
time_sum = 0.5  # 计算用每个间隔的时间长度(固定值）
# comment_data_location = r'data\test\comment_sum\\'  # 话题路径
title = '居民拒改昵称被移出业主群后起诉管理员'  # 话题名称
hotspots_boundary = 10  # 热度概率计算调整值（上线60）

log_total = 10  # 总评论数计算公式log值
log_maxH = 10  # 最多小时评论数计算公式log值
par_U_dc = 1  # 总评论数参数
par_U_c = 1  # 最多小时评论数参数
par_N = 5  # 媒体关注度除法分母参数（不能为零）


def run(comment_data_name, time_subsection, time_sum, time_num):
    wb = openpyxl.Workbook()
    ws = wb.active
    # 添加包含时间信息的标题行
    ws.append(
        ['Filename', 'Time Interval', '热度值', '热点事件概率', '用户关注度', '用户关注增长率', '总评论数量化值',
         '小时最评论数量化值',
         '媒体关注度',
         '话题敏感度', '用户情感值', '情感倾向'])

    # 构建完整文件路径
    full_path = os.path.join('data', 'test', 'comment_sum', comment_data_name + '.xlsx')

    time_intervals = []
    T_values = []
    hot_events_probability = []

    factor=int(time_num / time_sum)
    for i in range(1, time_subsection * factor + 1):
        # 计算当前时间段末尾的时间
        current_time = i * time_sum
        if current_time % time_num != 0:
            continue
        hours = int(current_time)
        minutes_with_seconds = (current_time - hours) * 60
        minutes = int(minutes_with_seconds)
        formatted_time_short = f"{hours}:{minutes}"
        seconds = int((minutes_with_seconds - minutes) * 60)
        formatted_time = f"{hours}:{minutes}:{seconds}"
        time_intervals.append(formatted_time_short)

        user_data_list = get_user_data_list(r'data\test\comment_sum\\' + comment_data_name + '.xlsx')
        U, increace_count, total_m, max_m = count_messages_in_timeframe(user_data_list, log_total, log_maxH, par_U_dc,
                                                                        par_U_c, i, current_time)
        if U == -1:
            T = 0
            print(f"========！！！{comment_data_name}-话题为空！！！========")
        else:
            news_data_list = get_news_data_list(r'data\test\comment\\' + comment_data_name)
            N = count_exceeding_messages(news_data_list, par_N, current_time)
            heat_level = classify_string(comment_data_name, 'dataset')
            # F = Cemotion_prodict(filename)
            emotion_data_list = get_emotion_data_list(r'data\test\comment_sum\\' + comment_data_name + '.xlsx')
            F = sum_emotion(emotion_data_list, current_time) * 10
            if F > 0:
                f = 1
            else:
                f = -1
                F = abs(F)
            T = heat_level * (U + N) * F

            if T < hotspots_boundary:
                hot_event = T
            elif T < 60:
                hot_event = hotspots_boundary + (T - hotspots_boundary) * (100 - hotspots_boundary) / (
                        60 - hotspots_boundary)
            else:
                hot_event = 99

            print(f"========{comment_data_name}  ---  第{i/factor}时间段 {formatted_time}h时间计算完成========")
        # 直接将结果写入Excel工作表
        ws.append(
            [comment_data_name, formatted_time, T, hot_event, U, increace_count, total_m, max_m, N, heat_level, F, f])
        T_values.append(T)
        hot_events_probability.append(hot_event)

    # 保存Excel工作簿
    wb.save(fr"data\analysis\{comment_data_name}_analysis.xlsx")

    # 绘制折线图

    plt.rcParams['font.family'] = 'SimHei'
    fig, ax1 = plt.subplots()  # 创建一个图和第一个y轴
    ax1.plot(time_intervals, T_values, 'g-')  # 绘制第一个数据集，例如用绿线
    ax1.set_xlabel('时间间隔（小时）')
    ax1.set_ylabel('热度值', color='g')  # 设置第一个y轴标签
    ax1.tick_params('y', colors='g')
    # for i, txt in enumerate(T_values):
    #     ax1.annotate(f'{txt:.2f}', (time_intervals[i], T_values[i]), textcoords="offset points", xytext=(0, 10),
    #                  ha='center', color='g')
    ax2 = ax1.twinx()  # 创建第二个y轴
    ax2.plot(time_intervals, hot_events_probability, 'b-')  # 在第二个y轴上绘制数据，例如用蓝线
    ax2.set_ylabel('热点事件概率', color='b')  # 设置第二个y轴标签
    ax2.tick_params('y', colors='b')
    for i, txt in enumerate(hot_events_probability):
        ax2.annotate(f'{txt:.1f}', (time_intervals[i], hot_events_probability[i]), textcoords="offset points",
                     xytext=(0, 10), ha='center', color='b')
    plt.title(f'{comment_data_name}中，每{time_num}h分段的热度值')
    plt.savefig(fr"data\analysis\{comment_data_name}_trend.png")
    plt.show()


if __name__ == '__main__':
    T = run(title, time_subsection, time_sum, time_num)
