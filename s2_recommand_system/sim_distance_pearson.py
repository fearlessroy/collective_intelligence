# coding=utf-8
from math import sqrt

critics = {'Tody': {'Snakes on a Plane': 4.5, 'You,Me and Dupree': 1.0, 'Superman Returns': 4.0},
           'Jack': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0,
                    'You,Me and Dupree': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0},
           'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                         'Superman Returns': 3.5,
                         'You,Me and Dupree': 2.5, 'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5,
                            'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You,Me and Dupree': 2.5}
           }


# 欧几里德距离
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
    print(res)
    return res


# 皮尔逊相关度评价
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
    print(res)
    return res


if __name__ == "__main__":
    sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
    sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
