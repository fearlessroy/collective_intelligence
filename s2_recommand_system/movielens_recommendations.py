# -*- coding=utf-8 -*-
from sim_distance_pearson import get_recommandations, sim_distance, sim_pearson


def load_movielens():
    # csv文件中各列分别是：movieId,title,genres
    # 获取文件标题
    movies = {}
    for line in open('movies.csv'):
        (id, title) = line.split('\n')[0].split(',')[0:2]
        movies[id] = title

    # 加载数据
    # csv文件中前四列分别是：userId,movieId,rating,timestamp
    prefs = {}
    for line in open('ratings.csv'):
        (user, movie_id, rating, ts) = line.split('\n')[0].split(',')[0:4]
        prefs.setdefault(user, {})
        prefs[user][movies[movie_id]] = float(rating)
    return prefs


'''
数据集来自 “http://www.grouplens.org/node/73”
'''
if __name__ == "__main__":
    prefs = load_movielens()
    rank = get_recommandations(prefs, '87')[:30]
    print rank
