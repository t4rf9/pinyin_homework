#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import json
import os
import re

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
non_Chinese = re.compile("[a-zA-Z0-9，。？：/【】「」；·～！@#¥%…&*（）—+\-=、｜|{}\[\]\"\':;,.<>?《》~`!$^()“” ]+")
sentence_list = []
for data in data_str_list:
    sentence_list.extend(re.split(non_Chinese, data))

# save sentence list
os.chdir('../')
with open("sentence_list.json", 'w') as outfile:
    json.dump(sentence_list, outfile)
    outfile.close()
