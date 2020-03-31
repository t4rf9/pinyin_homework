#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import json

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


def calc_freq2char(datatype):
    freq2char = {'E': {}}
    for char in char_pinyin.keys():
        freq2char[char] = {}
    with open("../../resources/" + datatype + "_list.json") as in_file:
        data_list = json.load(in_file)
        in_file.close()
    for data in data_list:
        data_len = len(data)
        if data_len > 0:
            if data[0] in freq2char:
                if 'S' in freq2char[data[0]]:
                    freq2char[data[0]]['S'] += 1
                else:
                    freq2char[data[0]]['S'] = 1

            i = 1
            while i < data_len and data[i - 1] not in freq2char:
                i += 1
            while i < data_len:
                if data[i] in freq2char:
                    if data[i - 1] in freq2char[data[i]]:
                        freq2char[data[i]][data[i - 1]] += 1
                    else:
                        freq2char[data[i]][data[i - 1]] = 1
                else:
                    i += 1
                i += 1

            if i == data_len:
                if data[-1] in freq2char['E']:
                    freq2char['E'][data[-1]] += 1
                else:
                    freq2char['E'][data[-1]] = 1

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

    with open("../../statistics/freq2char_" + datatype + ".json", 'w') as out_file:
        json.dump(freq2char, out_file)
        out_file.close()

    return freq2char


if __name__ == "__main__":
    # calc_freq1char()
    freq2sentence = calc_freq2char('sentence')
    freq2word = calc_freq2char('word')
