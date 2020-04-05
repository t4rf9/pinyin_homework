#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import json
import pypinyin

with open("../../resources/char_pinyinList_dict.json") as in_file:
    char_pinyin = json.load(in_file)
    in_file.close()


def calc_freq1char():
    freq1char = {}
    for char in char_pinyin.keys():
        freq1char[char] = 0
    with open("../../resources/sentence_list.json") as in_file:
        sentence_list = json.load(in_file)
        in_file.close()
    for sentence in sentence_list:
        for char in sentence:
            if char in freq1char:
                freq1char[char] += 1
    s = 0
    for i in freq1char.values():
        s += i
    for i in freq1char:
        freq1char[i] /= s
    with open("../../statistics/freq1char.json", 'w') as out_file:
        json.dump(freq1char, out_file)
        out_file.close()


def calc_freq2char(datatype, s=False, e=False):
    freq2char = {'E': {}} if e else {}
    for char in char_pinyin.keys():
        freq2char[char] = {}
    with open("../../resources/" + datatype + "_list.json") as in_file:
        data_list = json.load(in_file)
        in_file.close()
    for data_str in data_list:
        data_len = len(data_str)
        if data_len > 0:
            if s and data_str[0] in freq2char:
                if 'S' in freq2char[data_str[0]]:
                    freq2char[data_str[0]]['S'] += 1
                else:
                    freq2char[data_str[0]]['S'] = 1

            i = 1
            # find the first available character
            while i < data_len and data_str[i - 1] not in freq2char:
                i += 1

            # iteratively count
            while i < data_len:
                if data_str[i] in freq2char:
                    if data_str[i - 1] in freq2char[data_str[i]]:
                        freq2char[data_str[i]][data_str[i - 1]] += 1
                    else:
                        freq2char[data_str[i]][data_str[i - 1]] = 1
                else:
                    i += 1
                i += 1

            if e and i == data_len:
                if data_str[-1] in freq2char['E']:
                    freq2char['E'][data_str[-1]] += 1
                else:
                    freq2char['E'][data_str[-1]] = 1

    freq1char = {}
    for i in freq2char:
        for j in freq2char[i]:
            if j in freq1char:
                freq1char[j] += freq2char[i][j]
            else:
                freq1char[j] = freq2char[i][j]
    for i in freq2char:
        for j in freq2char[i]:
            freq2char[i][j] /= freq1char[j]

    with open("../../statistics/freq2char_" + datatype + ('_S' if s else '') + ('_E' if e else '') + ".json", 'w') \
            as out_file:
        json.dump(freq2char, out_file)
        out_file.close()

    return freq2char


def calc_freq3char(datatype, s=False, e=False):
    freq3char = {'E': {}} if e else {}
    for char in char_pinyin.keys():
        freq3char[char] = {}
    with open("../../resources/" + datatype + "_list.json") as in_file:
        data_list = json.load(in_file)
        in_file.close()
    for data_str in data_list:
        data_len = len(data_str)
        if data_len > 1:
            if s and data_str[0] in freq3char and data_str[1] in freq3char:
                if data_str[1] in freq3char[data_str[0]]:
                    freq3char[data_str[0]]['S'] += 1
                else:
                    freq3char[data_str[0]]['S'] = 1

            i = 1
            # find the first available character
            while i < data_len and data_str[i - 1] not in freq3char:
                i += 1

            # iteratively count
            while i < data_len:
                if data_str[i] in freq3char:
                    if data_str[i - 1] in freq3char[data_str[i]]:
                        freq3char[data_str[i]][data_str[i - 1]] += 1
                    else:
                        freq3char[data_str[i]][data_str[i - 1]] = 1
                else:
                    i += 1
                i += 1

            if e and i == data_len:
                if data_str[-1] in freq3char['E']:
                    freq3char['E'][data_str[-1]] += 1
                else:
                    freq3char['E'][data_str[-1]] = 1

    freq1char = {}
    for i in freq3char:
        for j in freq3char[i]:
            if j in freq1char:
                freq1char[j] += freq3char[i][j]
            else:
                freq1char[j] = freq3char[i][j]
    for i in freq3char:
        for j in freq3char[i]:
            freq3char[i][j] /= freq1char[j]

    with open("../../statistics/freq2char_" + datatype + ('_S' if s else '') + ('_E' if e else '') + ".json",
              'w') as out_file:
        json.dump(freq3char, out_file)
        out_file.close()

    return freq3char


if __name__ == "__main__":
    # calc_freq1char()
    freq2sentence = calc_freq2char('sentence', s=True, e=False)
    # freq2word = calc_freq2char('word', s=True, e=True)
    # freq2word = calc_freq2char('word', s=False, e=False)
