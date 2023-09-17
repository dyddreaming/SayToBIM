import csv

data = [
    ["物体名称", "属性"],
    ["长方体", "长,宽,高"],
    ["立方体", "边长"],
    ["球体", "半径"],
    ["圆柱体", "底面半径,高"],
    ["圆锥体", "底面半径,高"],
    ["三角形", "底边长,高,三边长,三角形类型"],
    ["矩形", "长,宽,对角线长度,角度"],
    ["圆形", "半径,直径,圆心坐标"],
    ["椭圆", "长轴,短轴,焦点坐标,离心率"],
    ["多边形", "边数,边长,角度,中心坐标"],
    ["平行四边形", "底边长,高,对角线长度,角度"],
    ["梯形", "上底,下底,高,两边斜率,对角线长度"],
    ["菱形", "对角线1,对角线2,角度"]
]

# 将数据写入CSV文件
with open('3d_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("CSV文件已生成。")