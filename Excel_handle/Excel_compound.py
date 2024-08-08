from datetime import datetime
import os
import pandas as pd

'''
将新闻汇总到一个大的话题文件中
'''

class ExcelMerger:
    '''
    将话题下的每个新闻评论表格汇总，汇总成话题总评论表格
    '''
    def __init__(self, source_folder, target_folder):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.merge_excel_files()

    # 添加一个方法来解析时间字符串
    def parse_date(self, date_str):
        return datetime.strptime(date_str, '%a %b %d %H:%M:%S +0800 %Y')

    def merge_excel_files(self):
        if not os.path.exists(self.target_folder):
            os.makedirs(self.target_folder)

        for subdir in next(os.walk(self.source_folder))[1]:
            subdir_path = os.path.join(self.source_folder, subdir)
            all_data = pd.DataFrame()

            for file in os.listdir(subdir_path):
                if file.endswith('.xlsx'):
                    file_path = os.path.join(subdir_path, file)
                    try:
                        df = pd.read_excel(file_path, engine='openpyxl')
                        # 检查是否存在'发布时间'列
                        if '发布时间' not in df.columns:
                            print(f"The column '发布时间' does not exist in {file_path}")
                            continue  # 跳过这个文件
                        all_data = all_data.append(df, ignore_index=True)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

            # 在尝试访问'发布时间'列前，先检查它是否存在
            if '发布时间' in all_data.columns:
                all_data['发布时间'] = all_data['发布时间'].apply(self.parse_date)
                all_data.sort_values('发布时间', inplace=True)
            else:
                print("The '发布时间' column was not found in any files.")
                continue  # 继续处理下一个子目录

            # 输出
            output_path = os.path.join(self.target_folder, f'{subdir}.xlsx')
            all_data.to_excel(output_path, index=False, engine='openpyxl')

            print(f"All Excel files in {subdir} have been merged and sorted into {output_path}")

if __name__ == '__main__':
    # 使用类
    source_folder = r'data\test\comment'  # 确保这是包含子文件夹的路径
    target_folder = r'data\test\comment_sum'  # 数据将被写入这个文件夹
    excel_merger = ExcelMerger(source_folder, target_folder)
