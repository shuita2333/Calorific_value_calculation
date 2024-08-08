
import pandas as pd
import os


def get_user_data_list(filename):
    # 读取Excel文件
    df = pd.read_excel(filename, engine='openpyxl')

    # 转换'发布时间'列为datetime类型（如果尚未是这种类型）
    df['发布时间'] = pd.to_datetime(df['发布时间'])

    # 对数据进行排序
    df.sort_values('发布时间', inplace=True)

    # 将DataFrame转换为列表，每个元素是一个包含'发布时间'和其他可能需要的列的记录
    data_list = df.to_dict('records')

    return data_list


def get_emotion_data_list(sheet_name):
    # 使用pandas读取Excel文件
    df = pd.read_excel(sheet_name, engine='openpyxl')

    # 确保"发布时间"和"emotion"列存在
    if '发布时间' not in df.columns or 'emotion' not in df.columns:
        raise ValueError("The provided DataFrame does not contain required '发布时间' or 'emotion' columns.")

    # 将"发布时间"列转换为datetime对象
    df['发布时间'] = pd.to_datetime(df['发布时间'])

    # 按照"发布时间"列对数据进行排序
    df.sort_values(by='发布时间', inplace=True)

    # 将DataFrame转换为列表，每个元素是一个包含发布时间和情感值的元组
    data_list = df[['发布时间', 'emotion']].values.tolist()

    return data_list



def get_news_data_list(folder_path):
    '''
    从每个文件中读取数据
    :param folder_path: 数据文件夹路径
    :return: 字典，键为文件名，值为含有每个文件数据的列表
    '''
    data_dict = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(folder_path, file_name)

            try:
                df = pd.read_excel(file_path, engine='openpyxl')
            except:
                print(f"Error reading {file_path}. Skipping.")
                continue

            if '发布时间' not in df.columns:
                print(f"The column '发布时间' does not exist in {file_name}. Skipping this file.")
                continue

            df['发布时间'] = pd.to_datetime(df['发布时间'], format='%a %b %d %H:%M:%S %z %Y')
            data_dict[file_name] = df.to_dict('records')

    return data_dict


if __name__ == '__main__':
    # filename = '00后开始在对联上整活了'  # 请替换成你文件的实际路径
    # filename = r'..\data\test\comment_sum\\' + filename + '.xlsx'
    # U = get_user_data_list(filename)
    # print(U)
    #
    # folder_path = r'..\data\test\comment\00后把新年的颜色玩明白了'  # 替换成你的文件夹路径
    # time_sum = 5
    # processed_data = get_news_data_list(folder_path)
    # print(processed_data)

    filename = '00后开始在对联上整活了'  # 请替换成你文件的实际路径
    filename = r'..\data\test\comment_sum\\' + filename + '.xlsx'
    U = get_emotion_data_list(filename)
    print(U)