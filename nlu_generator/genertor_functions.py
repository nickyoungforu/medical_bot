# -*- coding: utf-8 -*-
# @Time    : 18-10-26 下午4:08
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn

import random

with open('./data/Chinese_Names_Corpus.txt', 'r') as f:
    name_list = f.read().splitlines()

with open('./data/disease.txt', 'r') as f:
    disease_list = f.read().splitlines()

with open('./data/laboratory_indicator.txt', 'r') as f:
    laboratory_indicator_list = f.read().splitlines()

with open('./data/medical-record-number.txt', 'r') as f:
    medical_record_number_list = f.read().splitlines()

with open('./data/bed-number.txt', 'r') as f:
    bed_number_list = f.read().splitlines()

with open('./data/department.txt', 'r') as f:
    department_list = f.read().splitlines()

with open('./data/hospital-number.txt', 'r') as f:
    hospital_number_list = f.read().splitlines()

with open('./data/time.txt', 'r') as f:
    time_list = f.read().splitlines()

with open('./data/inspection_name.txt', 'r') as f:
    inspection_name_list = f.read().splitlines()


# base generator function
def patient_name():
    return random.choice(name_list)


def medical_record_number():
    return random.choice(medical_record_number_list)


def hospital_number():
    return random.choice(hospital_number_list)


def department():
    return random.choice(department_list)


def admission_time():
    return random.choice(time_list)


def bed_number():
    return random.choice(bed_number_list)


def inspection_name():
    return random.choice(inspection_name_list)


def laboratory_name():
    return None


def laboratory_indicator():
    return random.choice(laboratory_indicator_list)


def order_name():
    return random.choice(['临时医嘱', '长期医嘱'])


def disease_name():
    return random.choice(disease_list)


def guide_name():
    return None


def literature_name():
    return None


def inspection_time():
    return random.choice(time_list)