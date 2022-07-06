# encoding: utf-8
from config import vrp as config
from model.vrp import vrp_load

jiedian_number = config.jiedian_number
jiedian_wurenji_list = config.jiedian_wurenji_list.copy()
weight = config.weight_list
weigth_max = config.weight_max
juli_juzhen = config.juli_juzhen.copy()
cost_wurenji = config.cost_wurenji
print("节点数目:  {}".format(jiedian_number))
print("无人机可运送的节点:  {}".format(jiedian_wurenji_list))
list_routes, dict_uav_route = vrp_load(
    jiedian_number=jiedian_number, wurenji_jiedian=jiedian_wurenji_list, weight=weight, weight_most=weigth_max,
    juli_juzhen=juli_juzhen, cost_wurenji=cost_wurenji)
for i in range(len(list_routes)):
    print("卡车运输{}:  {}".format(i + 1, list_routes[i]))
for i in dict_uav_route.keys():
    print("无人机可参与的运输:  {},  {}".format(i, dict_uav_route[i]))

