import re
import csv
import chardet

def key_word(text):
    # 初始化geometry_vocab
    geometry_vocab = {}

    # 检测文件编码
    with open('3d_data.csv', 'rb') as rawdata:
        result = chardet.detect(rawdata.read(10000))

    # 获取检测到的编码格式
    file_encoding = result['encoding']

    # 使用检测到的编码格式打开文件
    with open('3d_data.csv', mode='r', encoding=file_encoding) as file:
        reader = csv.reader(file)
        next(reader)  # 跳过CSV文件的标题行
        for row in reader:
            geometry_name = row[0]
            attributes = row[1].split(',')
            geometry_vocab[geometry_name] = attributes

    # 初始化结果字典
    results = {}

    # 遍历文本中的词汇表
    for geometry, attributes in geometry_vocab.items():
        # 构建正则表达式模式，匹配物体
        pattern = rf"({geometry})"

        # 使用正则表达式查找匹配项
        matches = re.finditer(pattern, text)

        # 如果有匹配项，将其添加到结果字典中
        for match in matches:
            # 获取匹配到的物体名称
            geometry_name = match.group(1)

            # 初始化物体名的空字典
            if geometry_name not in results:
                results[geometry_name] = {}

            # 获取该物体对应的属性列表
            attributes = geometry_vocab[geometry_name]

            # 构建属性匹配正则表达式
            attr_pattern = rf"({'|'.join(attributes)})(\d+(?:\.\d+)?)"

            # 使用正则表达式查找匹配的属性
            attr_matches = re.findall(attr_pattern, text)

            if attr_matches:
                attr_values = {attr: float(value) for attr, value in attr_matches}
                results[geometry_name].update(attr_values)

    # 打印结果
    for geometry, attributes in results.items():
        print(f"{geometry}: {attributes}")

    return results

# if __name__ == '__main__':
#     text = "我要建立一个长方体，长4，宽2，高4，还需要一个立方体，边长3，以及一个球体，半径5。"
#     KeyWord(text)