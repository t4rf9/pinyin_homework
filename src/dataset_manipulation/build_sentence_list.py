#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

"""
This script manipulates the Chinese language materials.
All non-Chinese characters are considered separators of Chinese 'sentences' and are excluded by the use of re.split.
In the end, the Chinese 'sentences' are gathered in a list and saved in a json file for further usage.
"""

import json
import os
import re


def isChinese(char):
    return u'\u4e00' <= char <= u'\u9fa5'


# read in news data
article_list = []
os.chdir('../../resources/sina_news_gbk')
news_filenames = os.listdir()
re_filename = re.compile("^.*?(\.txt)$")
for filename in news_filenames:
    if re_filename.fullmatch(filename) is not None and filename != "README.txt":
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
sentence_list = []
for data in data_str_list:
    sentence_list.extend(re.split(non_Chinese, data))

# save sentence list
os.chdir('../')
with open("sentence_list.json", 'w') as outfile:
    json.dump(sentence_list, outfile)
    outfile.close()
