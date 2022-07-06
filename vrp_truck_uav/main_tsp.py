# encoding: utf-8
from config import tsp as config
from model.tsp import tsp_gg

jiedian_number = config.jiedian_number
wurenji_jiedian = config.wurenji_jiedian.copy()
juli_juzhen = config.juli_juzhen.copy()
cost_wurenji = config.cost_wurenji
print("节点数目:  {}".format(jiedian_number))
print("无人机可运送的节点:  {}".format(wurenji_jiedian))
kache_jiedian, wurenji = tsp_gg(jiedian_number=jiedian_number, wurenji_list_jiedian=wurenji_jiedian, juli_juzhen=juli_juzhen,
                                wurenji_cost=cost_wurenji)
print("卡车运输:  {}".format(kache_jiedian))
for i in wurenji.keys():
    print("无人机可参与的运输:  {},  {}".format(i, wurenji[i]))

