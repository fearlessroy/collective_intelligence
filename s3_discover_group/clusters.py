# -*- coding=utf-8 -*-

from math import sqrt


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


def pearson(v1, v2):
    # 简单求和
    sum1 = sum(v1)
    sum2 = sum(v2)

    # 求平方和
    sum1Sq = sum(pow(v, 2) for v in v1)
    sum2Sq = sum(pow(v, 2) for v in v2)

    # 求乘积之和
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # 计算 r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))

    '''
    皮尔逊相关度的计算结果在两者完全匹配的情况下为1.0，而在两者毫无关系的情况下则为0，
    '''
    if den == 0:
        return 0

    # 这里用1减是为了将相似度越大的两个元素之间的距离变得越小
    return 1.0 - num / den


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # 最开始的聚类就是数据集中的每一行
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # 遍历每一个配对，寻找最小距离
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distance来缓存距离的计算值
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # 计算两个聚类的平均值
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]

        # 建立新的聚类

        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest,
                               id=currentclustid)

        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]


def print_clust(clust, labels=None, n=0):
    # 利用缩进来建立层级布局
    for i in range(n):
        print ' '
    if clust.id < 0:
        # 负数代表这是一个分支
        print '-'
    else:
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]

    # 现在开始打印右侧分支和左侧分支
    if clust.left != None:
        print_clust(clust.left, labels=labels, n=n + 1)
    if clust.right != None:
        print_clust(clust.right, labels=labels, n=n + 1)


if __name__ == "__main__":
    blognames, words, data = read_flie('blogdata.txt')
    clust = hcluster(data)
    print_clust(clust, labels=blognames)
