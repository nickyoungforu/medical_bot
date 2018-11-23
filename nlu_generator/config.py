# -*- coding: utf-8 -*-
# @Time    : 18-10-26 下午4:22
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn

import copy
from nlu_generator.genertor_functions import *

subject_list = ['我']
adverbial_list = ['想', '要']
predicate_list = ['查', '看', '查询', '查看', '查找', '看一下', '查一下', ]
attribute_list = [[['姓名'], ['病历号'], ['住院号'], ['科室', '入院时间', '床号'], ['姓名', '入院时间']],
                  [['疾病诊断']],
                  [['送检时间'], ['检验指标_att'], ['检验指标_att', '送检时间'], ['医嘱类型']], ]
objects_list = ['患者信息', '电子病历', '检查报告', '检验报告', '检验指标', '异常指标', '医嘱信息', '相似患者',
                '相关文献', '相关指南', '收藏']

subject_inner_combine = False
adverbial_inner_combine = False
predicate_inner_combine = False
attribute_inner_combine = True
objects_inner_combine = False

generate_path = [
                ['subject', 'adverbial', 'predicate', 'attribute', 'objects'],
                ['subject', 'adverbial', 'predicate', 'objects'],
                ['adverbial', 'predicate', 'attribute', 'objects'],
                ['predicate', 'objects'],
                ['attribute', 'objects'],
                ['attribute'],
                ['objects'],
                ]
#
ban_rule_map = {'疾病诊断': {'患者信息', '电子病历', '检查报告', '检验报告', '检验指标', '异常指标', '医嘱信息', '收藏'},
                '检查报告名称': {'患者信息', '电子病历', '检验报告', '检验指标', '异常指标', '医嘱信息', '相似患者', '相关文献', '相关指南', '收藏'},
                # '检验报告名称': {'患者信息', '电子病历', '检查报告', '异常指标', '医嘱信息', '相似患者', '相关文献', '相关指南', },
                '送检时间': {'患者信息', '电子病历', '异常指标', '医嘱信息', '相似患者', '相关文献', '相关指南', '送检时间', '收藏'},
                '检验指标_att': {'患者信息', '电子病历', '检查报告', '异常指标', '医嘱信息', '相似患者', '相关文献', '相关指南', '收藏'},
                '医嘱类型': {'患者信息', '电子病历', '检验报告', '检查报告', '异常指标', '相似患者', '相关文献', '相关指南', '检验指标', '收藏'},
                '姓名': {'收藏'},
                '病历号': {'收藏'},
                '住院号': {'收藏'},
                '入院时间': {'收藏'},
                '科室': {'收藏'},
                '床号': {'收藏'},
                }

intent_map = {'患者信息': 'request_patient_info',
              '电子病历': 'request_patient_emr',
              '检查报告': 'request_patient_inspection_report',
              '检验报告': 'request_patient_laboratory_report',
              '检验指标': 'request_patient_laboratory_indicator',
              '异常指标': 'request_patient_abnormal',
              '医嘱信息': 'request_patient_Medical_order',
              '相似患者': 'request_similar_patient',
              '相关文献': 'request_related_literature',
              '相关指南': 'request_related_guide',
              '收藏': 'request_collect',
              '姓名': 'inform',
              '病历号': 'inform',
              '住院号': 'inform',
              '科室': 'inform',
              '入院时间': 'inform',
              '床号': 'inform',
              '疾病诊断': 'inform',
              '检查报告名称': 'inform',
              '检验报告名称': 'inform',
              '检验指标_att': 'inform',
              '医嘱类型': 'inform',
              }

slot_map = {'姓名': 'patient-name',
            '病历号': 'medical-record-number',
            '住院号': 'hospital-number',
            '科室': 'department',
            '入院时间': 'time',
            '床号': 'bed-number',
            '疾病诊断': 'disease-name',
            '检查报告名称': 'inspection-name',
            '检验报告名称': 'laboratory-name',
            '检验指标_att': 'laboratory-indicator',
            '医嘱类型': 'order-name',
            '送检时间': 'inspection-time',
            }

func_map = {'姓名': patient_name,
            '病历号': medical_record_number,
            '住院号': hospital_number,
            '科室': department,
            '入院时间': admission_time,
            '床号': bed_number,
            '疾病诊断': disease_name,
            '检查报告名称': inspection_name,
            '检验报告名称': laboratory_name,
            '检验指标_att': laboratory_indicator,
            '医嘱类型': order_name,
            '送检时间': inspection_time,
            }

skeleton2muscle = {
                   '姓名': ['%s,'],
                   '病历号': ['病历号：%s,', '病历号为%s,'],
                   '住院号': ['住院号：%s,', '住院号为%s,'],
                   '科室': ['科室：%s,', '科室为%s,', '%s,'],
                   '入院时间': ['入院时间：%s,', '入院时间为%s,'],
                   '床号': ['床号：%s,', '床号为%s,'],
                   '疾病诊断': ['%s'],
                   '检查报告名称': ['%s,'],
                   # '检验报告名称': ['%s'],
                   '检验指标_att': ['%s,'],
                   '医嘱类型': ['医嘱类型：%s,', '医嘱类型为%s,'],
                   '送检时间': ['送检时间：%s,', '送检时间为%s,'],
                   }


def ban_rule_set_gen():
    rule_set = []
    for k, vs in ban_rule_map.items():
        for v in vs:
            rule_set.append({k, v})
    return rule_set

ban_rules = ban_rule_set_gen()


def get_component(**kargs):
    combine = kargs['combine']
    component_list = kargs['com_list']
    if combine:
        com_index_rnd = random.random()
        if com_index_rnd < 0.7:
            com_item = copy.deepcopy(random.choice(component_list[0]))
            if random.random() > 0.7:
                com_item.extend(copy.deepcopy(random.choice(component_list[2])))

        elif com_index_rnd < 0.85:
            com_item = copy.deepcopy(random.choice(component_list[1]))
        else:
            com_item = copy.deepcopy(random.choice(component_list[2]))
    else:
        com_item = copy.deepcopy(random.choice(component_list))
    return com_item


if __name__ == '__main__':
    # print(ban_rules)
    # for i in range(1000):
    #     print(random.choice(attribute_list[0]))
    pass