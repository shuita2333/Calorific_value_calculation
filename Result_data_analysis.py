import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

'''
数据分析生成图像脚本
'''

def plot_excel_scatter(file_path):
    # 使用pandas读取Excel文件
    df = pd.read_excel(file_path)
    # 检查必要的列是否存在
    if 'Filename' in df.columns and '用户关注度' in df.columns:
        # 绘制散点图
        plt.figure(figsize=(10, 6))  # 设置图形大小
        plt.scatter(df['Filename'], df['用户关注度'], color='blue')  # 绘制散点图
        plt.title('Filename vs 用户关注度')  # 设置图形标题
        plt.xlabel('Filename')  # 设置x轴标签
        plt.ylabel('用户关注度')  # 设置y轴标签
        plt.xticks(rotation=45, ha="right")  # 旋转x轴标签，避免重叠
        plt.tight_layout()  # 自动调整子图参数, 使之填充整个图像区域
        plt.show()
    else:
        print("Excel文件中必须包含'Filename'和'用户关注度'这两列。")

# 使用示例
plot_excel_scatter('旧版热度值计算结果/V6.xlsx')
