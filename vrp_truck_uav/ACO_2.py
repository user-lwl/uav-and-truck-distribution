import random
import math
import numpy as np
import pandas as pd

# 导入距离
df = pd.read_excel("附件2_2.xlsx", sheet_name="问题2、问题3各地点之间距离（单位 公里）", index_col=0, header=0)
# 去除nan
df = df.fillna(9999, inplace=False)
# print(df)
# 城市数目，蚂蚁数目
city_number = 9
# 城市距离
distance_graph = [[0.0 for i in range(city_number)] for j in range(city_number)]
for i in range(city_number):
    for j in range(city_number):
        for x in range(1, city_number + 1):
            for y in range(1, city_number + 1):
                if i == x - 1 and j == y - 1:
                    distance_graph[i][j] = df[x][y]
# print(distance_graph)


class ACO(object):
    def __init__(self, city_number):
        self.ant_number = 1000
        self.aerfa = 2.0
        self.beita = 2.0
        self.rou = 0.1
        self.Q = 1
        self.city_number = city_number
        self.xinxisu_juzhen = np.zeros([city_number, city_number])
        self.ant_qun = [[0 for _ in range(city_number + 2)] for _ in range(self.ant_number)]
        self.flag = 1
        self.diedai_number = 100
        self.juli_juzhen = self.city_juli(city_number)
        self.qifahanshu = 10. / self.juli_juzhen
        self.len = None

    def init(self, juli_juzhen, number, city_number):
        start_place = 8
        lujing = []
        for i in range(number):
            r = [x for x in range(0, city_number)]
            if start_place >= city_number:
                start_place = random.randint(city_number)
                lujing.append(lujing[start_place].copy())
                continue
            cur = start_place
            r.remove(cur)
            lujing_1 = [cur]
            while len(r) != 0:
                t_min = math.inf
                xuanze = -1
                for x in r:
                    if juli_juzhen[cur][x] < t_min:
                        t_min = juli_juzhen[cur][x]
                        xuanze = x

                cur = xuanze
                lujing_1.append(xuanze)
                r.remove(xuanze)
            lujing.append(lujing_1)
            start_place += 1
        lujing_len = self.len(lujing)
        sort = np.argsort(lujing_len)
        ix = sort[0]
        lujing = lujing[ix]
        for i in range(len(lujing) - 1):
            s = lujing[i]
            s2 = lujing[i + 1]
            self.xinxisu_juzhen[s][s2] = 1
        self.xinxisu_juzhen[lujing[-1]][lujing[0]] = 1

    def lunpandu(self, p):
        x = np.random.rand()
        for i, t in enumerate(p):
            x -= t
            if x <= 0:
                break
        return i

    def ants(self, city_number):
        for i in range(self.ant_number):
            kaishi = np.random.randint(city_number - 1)
            self.ant_qun[i][0] = kaishi
            visit_not = list([x for x in range(city_number) if x != kaishi])
            visit_not.append(2)
            visit_not.append(3)
            # print(visit_not)
            cur = kaishi
            j = 1
            flag = 0
            while len(visit_not) != 0:
                xinxisu = []
                for v in visit_not:
                    xinxisu.append(self.xinxisu_juzhen[cur][v] ** self.aerfa * self.qifahanshu[cur][v] ** self.beita)
                xinxisu_sum = sum(xinxisu)
                xinxisu = [x / xinxisu_sum for x in xinxisu]
                ix = self.lunpandu(xinxisu)
                cur = visit_not[ix]
                self.ant_qun[i][j] = cur
                visit_not.remove(visit_not[ix])
                j += 1

    def city_juli(self, city_number):
        juli_juzhen = np.zeros((city_number, city_number))
        for i in range(city_number):
            for j in range(city_number):
                juli_juzhen[i][j] = distance_graph[i][j]
        #print(juli_juzhen)
        return juli_juzhen

    def lujing_len(self, path, juli_juzhen):
        a = path[0]
        b = path[-1]
        result = juli_juzhen[a][b]
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i + 1]
            result += juli_juzhen[a][b]
        return result

    def ant_len(self, path):
        r = []
        for one in path:
            len = self.lujing_len(one, self.juli_juzhen)
            r.append(len)
        return r

    def xinxisu_update(self):
        deerta_xinxisu = np.zeros([self.city_number, self.city_number])
        path = self.ant_len(self.ant_qun)
        for i in range(self.ant_number):
            for j in range(self.city_number - 1):
                a = self.ant_qun[i][j]
                b = self.ant_qun[i][j + 1]
                deerta_xinxisu[a][b] = deerta_xinxisu[a][b] + self.Q / path[i]
            a = self.ant_qun[i][0]
            b = self.ant_qun[i][-1]
            deerta_xinxisu[a][b] = deerta_xinxisu[a][b] + self.Q / path[i]
        self.xinxisu_juzhen = (1 - self.rou) * self.xinxisu_juzhen + deerta_xinxisu

    def aco(self):
        best_len = math.inf
        best_path = None
        for num in range(self.diedai_number):
            self.ants(self.city_number)
            self.len = self.ant_len(self.ant_qun)
            t_len = min(self.len)
            t_path = self.ant_qun[self.len.index(t_len)]
            if t_len < best_len:
                best_len = t_len
                best_path = t_path
            self.xinxisu_update()
            print("第{}次迭代，得到最短路径长度为{}".format(num + 1, best_len))
        return best_len, best_path, num

    def run(self):
        best_len, best_path, num = self.aco()
        return best_len, best_path, num


data = distance_graph
data = np.array(data)
while 1 == 1:
    aco = ACO(city_number=data.shape[0])
    Best, Best_path, num = aco.run()
    if data[Best_path[0]][Best_path[10]] != 9999:
        break
print("经过{}次迭代:".format(num + 1))
print("最短路径长度为：{}".format(Best))
for i in range(len(Best_path)):
    Best_path[i] = Best_path[i] + 1
print("最短路径为：{}".format(Best_path))


