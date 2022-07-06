# encoding: utf-8
import pandas as pd
import numpy as np

# 导入距离
df = pd.read_excel("附件2.xlsx", sheet_name="问题2、问题3各地点之间距离（单位 公里）", index_col=0, header=0)
# 去除nan
df = df.fillna(9999, inplace=False)
# print(df)
# 城市数目
city_number = 14
# 城市距离
distance_graph = [[0.0 for i in range(city_number)] for j in range(city_number)]
for i in range(city_number):
    for j in range(city_number):
        for x in range(1, 15):
            for y in range(1, 15):
                if i == x - 1 and j == y - 1:
                    distance_graph[i][j] = df[x][y]
data = np.array(distance_graph)
jiedian_number = 14
wurenji_jiedian_number = 6
wurenji_jiedian = [1, 3, 4, 11, 12, 13]
zuobiao_fanwei = (0, 100)
zuobiao = [(37.6010023, 15.05615328),
           (54.91818744, 33.40568245),
           (17.19063455, 70.45558097),
           (20.63348033, 54.1454275),
           (60.88213781, 56.64047713),
           (22.98864755, 24.4361699),
           (88.13502576, 37.80428478),
           (78.76480274, 4.77390268),
           (53.9449036, 7.11109909),
           (7.47424226, 32.0962852),
           (27.62339678, 39.8374327),
           (50.65573331, 30.54546097),
           (79.96097671, 37.58896454),
           (33.38277174, 27.85786219)]
qidian = (53.9449036, 7.11109909)
jiedian_list = [qidian] + zuobiao
juli_juzhen = data
cost_wurenji = 0.1


