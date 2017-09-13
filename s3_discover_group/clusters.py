# -*- coding=utf-8 -*-
import random

from math import sqrt

from PIL import Image, ImageDraw

'''
分级聚类通过连续不断地将最为相似的群组两两合并，来构造出一个群组的层级结构，
其中，每个群组都是从单一结构开始的。
'''


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


# 　皮尔逊相关度
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
    currentclust_id = -1

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
        new_cluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest,
                                id=currentclust_id)

        currentclust_id -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(new_cluster)

    return clust[0]


def print_clust(clust, labels=None, n=0):
    # 利用缩进来建立层级布局
    for i in range(n):
        print ' ',
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


# 定义聚类的总体高度
def get_height(clust):
    # 若是叶子节点，则高度为1
    if clust.left == None and clust.right == None:
        return 1

    # 否则高度为每个分支之和
    return get_height(clust.left) + get_height(clust.right)


# 定义根节点的总体误差
def get_depth(clust):
    # 一个叶节点的距离是0.0
    if clust.left == None and clust.right == None:
        return 0
    # 一个根节点的距离等于左右两侧分支中距离较大者
    # 加上该节点自身的距离
    return max(get_depth(clust.left), get_depth(clust.right)) + clust.distance


def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = get_height(clust.left) * 20
        h2 = get_height(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2

        # 线的长度
        l1 = clust.distance * scaling
        # 聚类到其子节点的垂直线
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

        # 连接左侧节点的水平线
        draw.line((x, top + h1 / 2, x + l1, top + h1 / 2), fill=(255, 0, 0))

        # 连接右侧节点的水平线
        draw.line((x, bottom - h2 / 2, x + l1, bottom - h2 / 2), fill=(255, 0, 0))

        # 调用函数绘制左右节点
        drawnode(draw, clust.left, x + l1, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + l1, bottom - h2 / 2, scaling, labels)
    else:
        # 如果这是叶节点，则绘制节点的标签
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


# 生成图片
def drawdendgram(clust, labels, jpeg='clusters.jpg'):
    # 高度和宽度
    h = get_height(clust) * 20
    w = 1200
    depth = get_depth(clust)

    # 由于宽度是固定的，因此我们需要对距离值做相应的调整
    scaling = float(w - 150) / depth

    # 新建一个白色背景的图片
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # 画第一个节点
    drawnode(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')


# 列聚类
def rotatematrix(data):
    new_data = []
    for i in range(len(data)):
        new_row = [data[j][i] for j in range(len(data))]
        new_data.append(new_row)
    return new_data


'''
K-均值聚类：
该算法首先会随机确定K个中心位置(位于空间中代表聚类中心的点)，然后将各个数据项分配给最临近的中心点。
待分配完成之后，聚类中心就会移动到分配给该聚类的所有节点的平均位置处，然后整个过程重新开始。
'''


def kcluster(rows, distance=pearson, k=4):
    # 确定每个点的最小值和最大值
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) for i in range(len(rows[0]))]

    # 随机创建k个点
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(rows[0]))] for j in
                range(k)]

    last_matches = None
    for t in range(100):
        print 'Iteration %d' % t
        best_matches = [[] for i in range(k)]

        # 在每行中寻找距离最近的中心点
        for j in range(len(rows)):
            row = rows[j]
            best_match = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[best_match], row):
                    best_match = i
            best_matches[best_match].append(j)
        # 如果结果与上一次相同，则整个过程结束
        if best_matches == last_matches:
            break
        last_matches = best_matches
        # 把中心点移动到所有成员的平均位置处
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(best_matches[i]) > 0:
                for rowid in best_matches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(best_matches[i])
                clusters[i] = avgs
    return best_matches


if __name__ == "__main__":
    blognames, words, data = read_flie('blogdata.txt')
    # clust = hcluster(data)
    # print_clust(clust, labels=blognames)
    # drawdendgram(clust, blognames, jpeg='blogclust.jpg')
    # rdata = rotatematrix(data)
    # wordclust = hcluster(rdata)
    # drawdendgram(wordclust, labels=words, jpeg='wordclust.jpg')
    # kclust = kcluster(data, k=10)
    # print [blognames[r] for r in kclust[0]]
