# -*- coding=utf-8 -*-

def read_flie(filename):
    lines = [line for line in file(filename)]

    # 第一行是列标题
    col_names = lines[0].strip().split('\t')[1:]
    row_names = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # 每行第一列是行名
        row_names.append(p[0])
        # 剩余部分就是该行对应的数据
        data.append([float(x) for x in p[1:]])
    return row_names, col_names, data


