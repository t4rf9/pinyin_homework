#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import json
import os
import jieba
import re

# read in news data
article_list = []
os.chdir('../../resources/sina_news_gbk')
news_filenames = os.listdir()
for filename in news_filenames:
    if filename != 'README.txt':
        with open(filename, 'r', encoding='gbk') as file:
            for line in file.readlines():
                article_list.append(json.loads(line))
            file.close()
os.chdir('../../resources/sina_news')
with open('2016-11.txt', 'r') as file:
    for line in file.readlines():
        article_list.append(json.loads(line))
    file.close()

# put text into a list
data_str_list = []
for article in article_list:
    data_str_list.append(article['title'])
    data_str_list.append(article['html'])
del article_list

# cut and filter non-Chinese characters
non_Chinese = re.compile("[^\u4e00-\u9fa5]+")
word_list = []
for data in data_str_list:
    tmp_word_list = jieba.lcut(data)
    for word in tmp_word_list:
        if len(word) == 0 or non_Chinese.match(word) is None:
            word_list.append(word)

# save word list
os.chdir('../')
with open("word_list.json", 'w') as outfile:
    json.dump(word_list, outfile)
    outfile.close()
