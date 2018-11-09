# -*- coding: utf-8 -*-
# @Time    : 18-10-25 下午4:07
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn

import json
import random
import copy
import nlu_generator.config as conf
import re





def nlu_generator(gen_num):
    nlu_data = {"rasa_nlu_data": {"common_examples": [],
                                  "regex_features": [],
                                  "entity_synonyms": [{"value": '', "synonyms": []}]
                                  }
                }
    generates_res = []
    count = 0
    while count < gen_num:
        sel_path = random.choice(conf.generate_path)
        singe_gen_complete = True
        single_gen_result = []
        for path_node in sel_path:
            com_list = getattr(conf, path_node + '_list')
            combine = getattr(conf, path_node + '_inner_combine')
            res = conf.get_component(**{'combine': combine, 'com_list': com_list})
            if isinstance(res, list):
                single_gen_result.extend(res)
            else:
                single_gen_result.append(res)
        # infrom
        if sel_path == ['attribute'] and len(single_gen_result) > 1:
            single_gen_result = [random.choice(single_gen_result)]
        for rule in conf.ban_rules:
            if rule == set(single_gen_result):
                singe_gen_complete = False
                break
            if rule.issubset(set(single_gen_result)) and len(rule) > 1:
                singe_gen_complete = False
                break

        if not singe_gen_complete:
            continue
        gen_transform = []
        entities = []
        intent = ''
        for i, gen_node in enumerate(single_gen_result):
            if gen_node in conf.intent_map:
                intent = conf.intent_map[gen_node]
            trans = gen_node if gen_node not in conf.func_map else conf.func_map[gen_node]()
            muscle_trans = trans if gen_node not in conf.skeleton2muscle else random.choice(conf.skeleton2muscle[gen_node]) % trans
            if len(single_gen_result) == 1:
                muscle_trans = trans
            if gen_node in conf.slot_map:
                start = len(''.join(gen_transform)) + muscle_trans.find(trans)
                end = start + len(trans)
                entities.append({"start": start,
                                 "end": end,
                                 "value": trans,
                                 "entity": conf.slot_map[gen_node]})
            gen_transform.append(muscle_trans)
        generates_res.append({"intent": intent,
                              "entities": entities,
                              "text": ''.join(gen_transform),
                              })
        print(''.join(gen_transform), intent, entities)
        count += 1
    # print(generates_res)
    nlu_data["rasa_nlu_data"]["common_examples"] = generates_res
    # print(json.dumps(nlu_data, indent=1))
    f = open('../data/nlu.json', 'w', encoding='utf-8')
    json.dump(nlu_data, f, indent=1, ensure_ascii=False)
    f.close()
    # print(nlu_data)

    return nlu_data



if __name__ == '__main__':
    # import IPython
    # IPython.embed()
    nlu_generator(3000)
    # print((getattr(conf, 'adverbial_list')))

