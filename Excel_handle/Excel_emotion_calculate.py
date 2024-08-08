import pandas as pd
import os

from cemotion import Cemotion
# os.environ["CUDA_VISIBLE_DEVICES"] = "3"

'''
情感信息预处理，预处理阶段分析每条评论情感，并存入数据表
'''

# 这个函数会读取指定文件夹中的所有Excel文件
def process_excel_comments(directory):
    # 首先计算目标扩展名文件的总数
    total_files = sum(1 for filename in os.listdir(directory) if filename.endswith('.xlsx'))
    current_file_number = 0  # 初始化当前文件计数器

    # 遍历指定目录下的所有文件
    i=0
    for filename in os.listdir(directory):
        i+=1

        # 检查文件扩展名是否是xlsx
        if filename.endswith('.xlsx'):
            current_file_number += 1  # 更新文件计数器

            # 构建文件的完整路径
            file_path = os.path.join(directory, filename)
            # 读取Excel文件
            df = pd.read_excel(file_path, engine='openpyxl')


            if "emotion" in df.columns:
                # if i % 10 == 0:
                #     print({i})
                print({i})
                continue

            # 检查“评论内容”列是否存在
            if "评论内容" in df.columns:
                # 假设Cemotion是一个定义好的类，用于情感分析
                c = Cemotion()

                # 处理每个评论
                df['emotion'] = df['评论内容'].apply(lambda x: c.predict(x))

                # 保存更改
                df.to_excel(file_path, index=False, engine='openpyxl')
            else:
                print(f"在文件 {file_path} 中没有找到'评论内容'列。")
            # 输出当前进度
            # print(f"已处理    {filename}     {current_file_number} / {total_files} 文件.")
            print(f"已处理    {filename}     {i} / {total_files} 文件.")




if __name__ == '__main__':
    # 假设你的文件夹路径是 'path_to_your_directory'
    # 你可以调用这个函数并传入实际的路径
    process_excel_comments('data/test/comment_sum')
    # process_excel_comments('data/test/c_test')
