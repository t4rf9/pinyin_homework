#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

"""
This script generates two dictionaries,
one with all Chinese characters of interest as keys and its all pinyins in a list as the value,
while the other with all pinyin as keys and all characters which can be paired with the pinyin as its value.
The two dictionaries are saved in json files.
"""

import json

char_dict = dict()
with open("../../resources/拼音汉字表_12710172/一二级汉字表.txt") as charFile:
    all_char = charFile.read()
    charFile.close()

for char in all_char:
    char_dict[char] = []
del all_char

pinyin_dict = dict()
with open("../../resources/拼音汉字表_12710172/拼音汉字表.txt") as pinyinFile:
    for line in pinyinFile.readlines():
        tmp = line.strip().split(' ')
        pinyin_dict[tmp[0]] = []
        for char in tmp[1:]:
            if char in char_dict:
                char_dict[char].append(tmp[0])
                pinyin_dict[tmp[0]].append(char)

    pinyinFile.close()

with open("../../resources/char_pinyinList_dict.json", 'w') as out:
    json.dump(char_dict, out)
    out.close()

with open("../../resources/pinyin_charList_dict.json", 'w') as out:
    json.dump(pinyin_dict, out)
    out.close()
