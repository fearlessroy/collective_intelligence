# -*- coding=utf-8 -*-

import feedparser
import re


# 返回一个RSS订阅源的标题和包含单词计数情况的字典
def get_word_counts(url):
    # 解析订阅源
    d = feedparser.parse(url)
    word_count = {}

    # 循环遍历所有的文章条目
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description  # summary 文章内容

        # 提取一个单词列表
        words = get_words(e.title + ' ' + summary)
        for word in words:
            word_count.setdefault(word, 0)
            word_count[word] += 1
    return d.feed.title, word_count


# 提取单词列表
def get_words(html):
    # 去除所有HTML标记
    txt = re.compile(r'<[^>]+>').sub('', html)

    # 利用所有非字母符拆分出单词
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # 转化成小写形式
    return [word.lower() for word in words if word != '']


apcount = {}  # 出现某单词的博客数目
wordcounts = {}
feedlist = [line for line in file('feedlist.txt')]
for feed_url in feedlist:
    title, word_count = get_word_counts(feed_url)
    wordcounts[title] = word_count
    for word, count in word_count.items():
        apcount.setdefault(word, 0)
        if count > 1:
            apcount[word] += 1

word_list = []
for w, bc in apcount.items():
    frac = float(bc) / len(feedlist)
    if frac > 0.1 and frac < 0.5:
        word_list.append(w)

out = file('blog_data.txt', 'w')
out.write('Blog')
for word in word_list:
    out.write('\t%s' % word)
out.write('\n')
for blog, wc in wordcounts.items():
    out.write(blog)
    for word in word_list:
        if word in wc:
            out.write('\t%d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')
