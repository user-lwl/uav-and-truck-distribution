# encoding: utf-8
from typing import List, Dict, Tuple
from gurobipy import *


def vrp_load(jiedian_number: int, wurenji_jiedian: List[int], weight: List[int], weight_most: int,
             juli_juzhen: List[List[int]], cost_wurenji: float = 0.5) \
        -> Tuple[List[List[int]], Dict[int, Tuple[int, int]]]:
    print("VRP")
    model = Model('vrp_load')
    x = model.addVars([(i, j) for i in range(0, jiedian_number + 1) for j in range(0, jiedian_number + 1)], vtype=GRB.BINARY,
                      name='x_')
    y = model.addVars([(i, j) for i in range(0, jiedian_number + 1) for j in range(0, jiedian_number + 1)], vtype=GRB.BINARY,
                      name='y_')
    s = model.addVars([i for i in range(1, jiedian_number + 1)], vtype=GRB.BINARY, name='s_')
    z = model.addVars([(i, j) for i in range(0, jiedian_number + 1) for j in range(0, jiedian_number + 1)], ub=weight_most,
                      vtype=GRB.CONTINUOUS, name='a_')
    for i in range(1, jiedian_number + 1):
        if i not in wurenji_jiedian:
            model.addConstr(quicksum(x[j, i] for j in range(0, jiedian_number + 1)) == 1, name='cons_1_in_x_[{}]'.format(i))
            model.addConstr(quicksum(x[i, j] for j in range(0, jiedian_number + 1)) == 1, name='cons_1_out_x_[{}]'.format(i))
        else:
            model.addConstr(quicksum(x[j, i] + y[j, i] for j in range(0, jiedian_number + 1)) == 1,
                            name='cons_1_in_xy_[{}]'.format(i))
            model.addConstr(quicksum(x[i, j] + y[i, j] for j in range(0, jiedian_number + 1)) == 1,
                            name='cons_1_out_xy_[{}]'.format(i))
            model.addConstr(quicksum(y[j, i] for j in range(0, jiedian_number + 1))
                            == quicksum(y[i, j] for j in range(0, jiedian_number + 1)), name='cons_1_y[{}]'.format(i))
    model.addConstr(quicksum(x[i, i] for i in range(0, jiedian_number + 1)) == 0, name='cons_2_x')
    model.addConstr(quicksum(y[i, i] for i in range(0, jiedian_number + 1)) == 0, name='cons_2_y')
    for i in range(1, jiedian_number + 1):
        model.addConstr(s[i] == quicksum(x[i, j] for j in range(0, jiedian_number + 1)), name='cons_3_[{}]'.format(i))
    big_m = 10 ** 6
    for j in range(1, jiedian_number + 1):
        for i in range(0, jiedian_number + 1):
            list_not_j = list(range(0, j)) + list(range(j + 1, jiedian_number + 1))
            list_uav_not_j = wurenji_jiedian.copy()
            if j in list_uav_not_j:
                list_uav_not_j.remove(j)
            model.addConstr(z[i, j] >= weight[j - 1] + quicksum(z[j, k] for k in list_not_j)
                            + quicksum(y[j, u] * weight[u - 1] for u in list_uav_not_j) + (x[i, j] - 1) * big_m,
                            name='cons_4_[{},{}]'.format(i, j))

            model.addConstr(z[i, j] <= x[i, j] * big_m, name='cons_4_zx_[{},{}]'.format(i, j))
            if i:
                model.addConstr(x[i, j] + x[j, i] <= 1, name='cons_4_loop_2[{},{}]'.format(i, j))
    for j in wurenji_jiedian:
        for i in range(0, jiedian_number + 1):
            for k in range(0, jiedian_number + 1):
                model.addConstr(y[i, j] + y[j, k] <= 75 * 70 / 60, name='cons_5_[{},{},{}]'.format(i, j, k))
    for i in range(0, jiedian_number + 1):
        model.addConstr(quicksum(y[i, j] for j in range(0, jiedian_number + 1)) <= 1, name='cons_6_out_[{}]'.format(i))
        model.addConstr(quicksum(y[j, i] for j in range(0, jiedian_number + 1)) <= 1, name='cons_6_in_[{}]'.format(i))
    model.addConstr(quicksum(x[0, j] for j in range(1, jiedian_number + 1)) >= math.ceil(sum(weight) / weight_most),
                    name='cons_7')
    num_vehicle = quicksum(x[0, j] for j in range(1, jiedian_number + 1))
    sum_distance = quicksum(x[i, j] * juli_juzhen[i][j] + y[i, j] * juli_juzhen[i][j] * cost_wurenji
                            for i in range(0, jiedian_number) for j in range(0, jiedian_number))
    model.setObjective(num_vehicle * big_m + sum_distance, sense=GRB.MINIMIZE)
    model.setParam(GRB.Param.TimeLimit, 600)
    model.setParam(GRB.Param.MIPGap, 0.05)
    model.optimize()
    x_ = model.getAttr('X', x)
    y_ = model.getAttr('X', y)
    s_ = model.getAttr('X', s)
    num_vehicle_ = int(sum(x_[0, j] for j in range(1, jiedian_number + 1)))
    print("车次数: {}".format(num_vehicle_))
    wurenji_jiedian_list = []
    wurenji_list = {}
    for j in wurenji_jiedian:
        if s_[j] < 0.1:
            wurenji_jiedian_list.append(j)

            fr, to = None, None
            for i in range(0, jiedian_number + 1):
                if y_[i, j] > 0.9:
                    fr = i
                    break
            for k in range(0, jiedian_number + 1):
                if y_[j, k] > 0.9:
                    to = k
                    break
            tup_fr_to = (fr, to)
            wurenji_list[j] = tup_fr_to
    print("无人机可以到达的节点:  {}".format(wurenji_jiedian))
    print("无人机送货的节点:  {}".format(wurenji_jiedian_list))
    kache_list = []
    set_node = set(range(0, jiedian_number + 1))
    while len(set_node) > 1 + len(wurenji_jiedian_list):
        list_route_cur = [0]
        to = None
        while to != 0:
            if to:
                set_node.remove(to)
            for i in set_node:
                if x_[list_route_cur[-1], i] > 0.9:
                    to = i
                    list_route_cur.append(to)
                    break
        kache_list.append(list_route_cur)
    return kache_list, wurenji_list

