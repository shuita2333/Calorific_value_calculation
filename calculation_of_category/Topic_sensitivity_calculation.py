import os
'''
话题敏感度计算函数
'''
def classify_string(input_string, folder_path):
    '''
    话题敏感度计算函数
    :param input_string: 话题名
    :param folder_path: 敏感词库路径
    :return: heat_level 敏感度等级
    '''
    print("话题敏感度计算中。。。")
    # 遍历文件夹中的所有文件
    heat_level = 1
    heat_category = 0
    level = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            # print(file_path)            # 打开文件并读取行
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # 移除行尾的换行符并检查词语是否在输入字符串中
                    word = line.strip()
                    if word in input_string:
                        # 如果找到匹配，则返回对应的文件名作为类别
                        filename=filename.replace('.txt', '')  # 文件名代表类别
                        if filename=='反动':
                            level=0.25
                        elif filename=='暴恐':
                            level=0.5
                        elif filename=='民生':
                            level=0.75
                        elif filename=='贪腐':
                            level=0.5
                        heat_level=heat_level+level
                        heat_category=heat_category+1
                        break
    # 如果没有找到匹配，返回None
    if heat_category == 0 or heat_category == 1:
        return heat_level
    heat_level=heat_level*(1-heat_category*0.1)
    return heat_level

if __name__ == '__main__':
    # 测试函数
    category = classify_string("这是一个", "../dataset")
    print(f'属于类别等级为: {category}')

