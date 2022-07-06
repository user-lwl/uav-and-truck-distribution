# encoding: utf-8
import pandas as pd
import numpy as np

# 导入距离
#df = pd.read_excel("附件2.xlsx", sheet_name="问题2、问题3各地点之间距离（单位 公里）", index_col=0, header=0)
df = pd.read_excel("附件3_x.xlsx", sheet_name="问题4各地点之间距离（单位  公里）", index_col=0, header=0)
# 去除nan
df = df.fillna(9999, inplace=False)
# print(df)
# 城市数目
city_number = 16
# 城市距离
distance_graph = [[0.0 for i in range(city_number)] for j in range(city_number)]
for i in range(city_number):
    for j in range(city_number):
        for x in range(1, 17):
            for y in range(1, 17):
                if i == x - 1 and j == y - 1:
                    distance_graph[i][j] = df[x][y]
data = np.array(distance_graph)
jiedian_number = 16
jiedian_wurenji_number = 7
jiedian_wurenji_list = [17 - 14, 18 - 14, 19 - 14, 23 - 14, 24 - 14, 28 - 14, 29 - 14]
zuobiao_fanwei = (0, 100)
#zuobiao = [(37.6010023, 15.05615328),
#           (54.91818744, 33.40568245),
#           (17.19063455, 70.45558097),
#           (20.63348033, 54.1454275),
#           (60.88213781, 56.64047713),
#           (22.98864755, 24.4361699),
#           (88.13502576, 37.80428478),
#           (78.76480274, 4.77390268),
#           (53.9449036, 7.11109909),
#           (7.47424226, 32.0962852),
#           (27.62339678, 39.8374327),
#           (50.65573331, 30.54546097),
#           (79.96097671, 37.58896454),
#           (33.38277174, 27.85786219)]
#qidian = (53.9449036, 7.11109909)
#jiedian_list = [qidian] + zuobiao
juli_juzhen = data
cost_wurenji = 0.1
upper_weight_item = 500
#weight_list = [12, 90, 24, 15, 70, 18, 150, 50, 30, 168, 36, 44, 42, 13]
weight_list = [41, 76, 12, 16, 19, 12, 33, 15, 27, 13, 85, 74, 120, 48, 35, 180]
weight_max = 500
print("总重量:  {}".format(sum(weight_list)))

