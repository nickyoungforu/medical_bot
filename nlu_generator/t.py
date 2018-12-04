# -*- coding: utf-8 -*-
# @Time    : 18-10-26 上午10:58
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn

import json
import re
import random
# a = set()
# with open("laboratory_indicator_unfiltered.txt", "r") as f:
#     a = f.read().splitlines()
# # a = list(a)
# for i in range(len(a)):
#     a[i] = re.sub("[\(（][^\)）]+[\)）]", '', a[i])
# # for i in range(len(a)):
# #     a[i] = re.sub("/\（.*\）/", '', a[i])
# # for i in range(len(a)):
# #     a[i] = re.sub(" ", '', a[i])
# with open("laboratory_indicator_unfiltered2.txt", 'w') as f:
#     f.write('\n'.join(a))

# with open("laboratory_indicator_unfiltered2.txt", "r") as f:
#     a = set(f.read().splitlines())
#
# with open("laboratory_indicator_unfiltered3.txt", 'w') as f:
#     f.write('\n'.join(list(a)))

import random
a = set()
for i in range(2000):
    year = random.randint(2016, 2018)
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    if random.random()>0.5:
        a.add(str(year) + '年' + str(month) + '月' + str(day) + '号')
    else:
        a.add(str(year)+'年'+str(month)+'月'+str(day)+'日')
with open("time.txt", 'w') as f:
    f.write('\n'.join(list(a)))

# a = []
# with open("./data/inspection_name_unfiltered.txt", "r") as f:
#     a = f.read().splitlines()
# # a = list(a)
# b = []
# for i in range(len(a)):
#     a[i] = re.sub("\+|＋|，|\|", ',', a[i])
#     a[i] = re.sub("[\(（][^\)）]+[\)）]", '', a[i])
#     b.extend(a[i].split(','))
# # for i in range(len(a)):
# #     a[i] = re.sub("/\（.*\）/", '', a[i])
# # for i in range(len(a)):
# #     a[i] = re.sub(" ", '', a[i])
# b = set(b)
# with open("./data/inspection_name.txt", 'w') as f:
#     f.write('\n'.join(list(b)))