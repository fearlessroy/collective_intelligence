# coding=utf-8
from math import sqrt

'''
协作型过滤：对一大群人进行搜索，并从中找出与我们品味相近的一小群人。
分为：
    基于用户的协作型过滤：适用于规模较小但比变化频繁的内存数据集
    基于物品的协作型过滤：稀疏数据集优先选择
对于密集型数据集而言，两者效果都是一样的
基于物品：物品间的比较不会像用户间的比较那么频繁，这意味着无需不停地计算与每样物品最为相近的其他物品，我们可以将这些运算任务
安排在网络流量不是很大的时候进行，或者独立于主应用之外的另一台计算机上单独执行。
'''
# 数据集
critics = {'Tody': {'Snakes on a Plane': 4.5, 'You,Me and Dupree': 1.0, 'Superman Returns': 4.0},
           'Jack': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0,
                    'You,Me and Dupree': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0},
           'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                         'Superman Returns': 3.5,
                         'You,Me and Dupree': 2.5, 'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5,
                            'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You,Me and Dupree': 2.5},
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5,
                                'The Night Listener': 4.0}
           }


# 欧几里德距离，平方和求根
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0

    sum_of_squares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])

    res = 1 / (1 + sqrt(sum_of_squares))
    return res


# 皮尔逊相关度评价,两组数据与某条直线的拟合程度
def sim_pearson(prefs, p1, p2):
    # 得到双方都评价过的物品列表
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    n = len(si)
    # 如果两者没有共同喜好，则返回1
    if n == 0:
        return 1
    # 对所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # 求平方和
    sum1_sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2_sq = sum([pow(prefs[p2][it], 2) for it in si])

    # 求乘积之和
    p_sum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # 计算皮尔逊相关值
    num = p_sum - (sum1 * sum2 / n)
    den = sqrt((sum1_sq - pow(sum1, 2) / n) * (sum2_sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    res = num / den
    return res  # 值为1则表示两个人对每一样物品均有着完全一致的评价


# 从反映偏好的字典中返回最为匹配者
# 返回结果的个数和相似度函数均为可选参数
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    # 对列表进行排序，评价值最高者排在前面
    scores.sort()
    scores.reverse()
    return scores[0:n]


# 利用所有他人评价值的加权平均，为某人提供建议
def get_recommandations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # 不和自己做比较
        if other == person:
            continue
        sim = similarity(prefs, person, other)

        # 忽略评价值为0或小于0的情况
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                # 相似度*评价值
                totals[item] += prefs[other][item] * sim
                # 相似度之和
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings  # 返回自己没有看过影片的预期评价情况，从高到底n个


# 键值对调
def transform_prefs(prefs):  # 基于物品
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    # print result
    return result


if __name__ == "__main__":
    sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
    sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
    top_matches(critics, 'Tody', n=3)
    get_recommandations(critics, 'Tody')
    get_recommandations(critics, 'Tody', similarity=sim_distance)
    movies = transform_prefs(critics)
    top_matches(movies, 'Superman Returns')
