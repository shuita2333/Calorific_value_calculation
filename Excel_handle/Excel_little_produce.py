import os
import shutil
import pandas as pd

'''
生成little版数据集，将大话题抽取其中第一条新闻组成由“little_”开头的小话题
'''

def copy_first_excel_file(src_dir, dest_dir):
    '''
    普通事件少文本生成
    :param src_dir: 原目录
    :param dest_dir: 生成后存储目录
    :return:
    '''
    os.makedirs(dest_dir, exist_ok=True)  # 确保目标目录存在

    # 遍历源目录中的所有子目录
    for folder_name in os.listdir(src_dir):
        folder_path = os.path.join(src_dir, folder_name)

        # 确保这是一个文件夹
        if os.path.isdir(folder_path):
            # 排列文件夹内的所有文件并拿到第一个Excel文件
            files = sorted([f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')])

            if files:
                first_excel_file = files[0]  # 获取第一个Excel文件
                excel_file_path = os.path.join(folder_path, first_excel_file)

                # 读取Excel文件
                df = pd.read_excel(excel_file_path)

                # 创建目标子文件夹
                new_folder_name = f"little_{folder_name}"
                new_folder_path = os.path.join(dest_dir, new_folder_name)
                os.makedirs(new_folder_path, exist_ok=True)

                # 指定新的文件路径
                new_excel_file_path = os.path.join(new_folder_path, f"little_{first_excel_file}")

                # 保存Excel文件到新的文件夹
                df.to_excel(new_excel_file_path, index=False)

                print(f"Copied '{first_excel_file}' to '{new_excel_file_path}'")
            else:
                print(f"No Excel files found in '{folder_name}'")
        else:
            print(f"'{folder_name}' is not a directory, skipping...")


# 使用函数
# 注意替换'src_dir'和'dest_dir'为你的源目录和目标目录路径
copy_first_excel_file('data/comment', '../data/test/comment')
