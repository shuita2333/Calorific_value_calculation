# 按文本字符串分析
from cemotion import Cemotion
import pandas as pd

'''
情感值计算函数，用于在过程中读入情感值并进行计算
速度较慢，现已废弃
'''
def extract_texts_from_excel_column(file_path, column_name):
    """
    从指定的Excel文件中的特定列提取所有文本内容。

    参数:
    file_path (str): Excel文件的路径。
    column_name (str): 需要提取文本的列的名称。

    返回:
    list: 包含指定列中所有文本内容的列表。
    """
    # 使用pandas读取Excel文件
    df = pd.read_excel(file_path, engine='openpyxl')

    # 确保列名存在于DataFrame中
    if column_name in df.columns:
        # 提取指定列的内容到列表
        texts = df[column_name].tolist()
        # 过滤掉任何非字符串的内容
        texts = [text for text in texts if isinstance(text, str)]
        return texts
    else:
        print(f"列 '{column_name}' 不存在于Excel文件中。")
        return []

def Cemotion_prodict(file_path):
    file_path=r'data\test\comment_sum\\' + file_path+'.xlsx'
    texts = extract_texts_from_excel_column(file_path, '评论内容')
    c = Cemotion()
    data=c.predict(texts)
    sum_value = sum(item[1] for item in data)
    sum_value=(sum_value-0.5)*5/len(texts)
    return sum_value

# 使用示例
if __name__ == '__main__':
    print(Cemotion_prodict('little_12岁男孩超重30斤患脂肪肝'))


# str_text1 = '配置顶级，不解释，手机需要的各个方面都很完美'
# str_text2 = '院线看电影这么多年以来，这是我第一次看电影睡着了。简直是史上最大烂片！没有之一！侮辱智商！大家小心警惕！千万不要上当！再也不要看了！'
#
# list_text = ['内饰蛮年轻的，而且看上去质感都蛮好，貌似本田所有车都有点相似，满高档的！',
# '总而言之，是一家不会再去的店。']
#
# c = Cemotion()
# print(c.predict(list_text))