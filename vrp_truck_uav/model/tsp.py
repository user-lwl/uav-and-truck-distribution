# encoding: utf-8
from typing import List, Dict, Tuple
from gurobipy import *


def tsp_gg(jiedian_number: int, wurenji_list_jiedian: List[int], juli_juzhen: List[List[int]], wurenji_cost: float = 0.5) \
        -> Tuple[List[int], Dict[int, Tuple[int, int]]]:
    print("TSP")
    model = Model('tsp_gg')
    x = model.addVars([(i, j) for i in range(0, jiedian_number + 1) for j in range(0, jiedian_number + 1)], vtype=GRB.BINARY,
                      name='x_')
    y = model.addVars([(i, j) for i in range(0, jiedian_number + 1) for j in range(0, jiedian_number + 1)], vtype=GRB.BINARY,
                      name='y_')
    s = model.addVars([i for i in range(1, jiedian_number + 1)], vtype=GRB.BINARY, name='s_')
    a = model.addVars([(i, j) for i in range(0, jiedian_number + 1) for j in range(0, jiedian_number + 1)], vtype=GRB.CONTINUOUS,
                      name='a_')
    for i in range(0, jiedian_number + 1):
        if i not in wurenji_list_jiedian:
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
    for i in range(1, jiedian_number + 1):
        list_n_i = list(range(0, i)) + list(range(i + 1, jiedian_number + 1))
        list_n_i_ori = list(range(1, i)) + list(range(i + 1, jiedian_number + 1))
        model.addConstr(quicksum(a[i, j] for j in list_n_i) - quicksum(a[j, i] for j in list_n_i_ori) == s[i],
                        name='cons_4_a_[{}]'.format(i))
        for j in range(0, jiedian_number + 1):
            model.addConstr(a[i, j] <= jiedian_number * x[i, j], name='cons_4_ax_[{},{}]'.format(i, j))
    for j in wurenji_list_jiedian:
        for i in range(0, jiedian_number + 1):
            for k in range(0, jiedian_number + 1):
                model.addConstr(y[i, j] + y[j, k] <= 75 * 70 / 60, name='cons_5_[{},{},{}]'.format(i, j, k))
    for i in range(0, jiedian_number + 1):
        model.addConstr(quicksum(y[i, j] for j in range(0, jiedian_number + 1)) <= 1, name='cons_6_out_[{}]'.format(i))
        model.addConstr(quicksum(y[j, i] for j in range(0, jiedian_number + 1)) <= 1, name='cons_6_in_[{}]'.format(i))
    cost = quicksum(x[i, j] * juli_juzhen[i][j] + y[i, j] * juli_juzhen[i][j] * wurenji_cost
                    for i in range(0, jiedian_number) for j in range(0, jiedian_number))
    model.setObjective(cost, sense=GRB.MINIMIZE)
    model.setParam(GRB.Param.TimeLimit, 300)
    model.setParam(GRB.Param.MIPGap, 0.02)
    model.optimize()
    x_ = model.getAttr('X', x)
    y_ = model.getAttr('X', y)
    s_ = model.getAttr('X', s)
    kache_jiedian = [0]
    to = None
    while to != 0:
        for i in range(0, jiedian_number + 1):
            if x_[kache_jiedian[-1], i] > 0.9:
                to = i
                kache_jiedian.append(i)
                break
    list_node_uav_ = []
    wurenji_jiedian = {}
    for j in wurenji_list_jiedian:
        if s_[j] < 0.1:
            list_node_uav_.append(j)

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
            wurenji_jiedian[j] = tup_fr_to
    print("无人机可到达的节点:  {}".format(wurenji_list_jiedian))
    print("无人机送货的节点:  {}".format(list_node_uav_))
    return kache_jiedian, wurenji_jiedian

