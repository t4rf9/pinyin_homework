#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import json
import pypinyin as PY
import random


def calc_freq1():
    freq1 = {}
    for char in char_pinyin.keys():
        freq1[char] = 0
    with open("../../resources/sentence_list.json") as in_file:
        sentence_list = json.load(in_file)
        in_file.close()
    for sentence in sentence_list:
        for char in sentence:
            if char in freq1:
                freq1[char] += 1
    s = 0
    for i in freq1.values():
        s += i
    for i in freq1:
        freq1[i] /= s
    try:
        out_file = open("../../statistics/freq1.json", 'w')
        json.dump(freq1, out_file)
        out_file.close()
    finally:
        return freq1


def calc_freq1_pinyin():
    freq1 = {}
    for char, char_pinyin_list in char_pinyin.items():
        for pinyin in char_pinyin_list:
            freq1[char + '_' + pinyin] = 0
    with open("../../resources/sentence_list.json") as in_file:
        sentence_list = json.load(in_file)
        in_file.close()
    for sentence in sentence_list:
        sentence_len = len(sentence)
        sentence_pinyin = PY.lazy_pinyin(sentence)
        for i in range(0, sentence_len):
            curr_char_pinyin = sentence[i] + '_' + sentence_pinyin[i]
            if curr_char_pinyin in freq1:
                freq1[curr_char_pinyin] += 1
    s = 0
    for i in freq1.values():
        s += i
    for i in freq1:
        freq1[i] /= s
    try:
        out_file = open("../../statistics/freq1_pinyin.json", 'w')
        json.dump(freq1, out_file)
        out_file.close()
    finally:
        return freq1


def calc_freq2(datatype, s=True, e=True):
    freq2 = {'E': {}} if e else {}
    for char in char_pinyin.keys():
        freq2[char] = {}
    with open("../../resources/" + datatype + "_list.json") as in_file:
        data_list = json.load(in_file)
        in_file.close()
    for data_str in data_list:
        data_len = len(data_str)
        if data_len > 0:
            if s and data_str[0] in freq2:
                if 'S' in freq2[data_str[0]]:
                    freq2[data_str[0]]['S'] += 1
                else:
                    freq2[data_str[0]]['S'] = 1

            i = 1
            # find the first available character
            while i < data_len and data_str[i - 1] not in freq2:
                i += 1

            # iteratively count
            while i < data_len:
                if data_str[i] in freq2:
                    if data_str[i - 1] in freq2[data_str[i]]:
                        freq2[data_str[i]][data_str[i - 1]] += 1
                    else:
                        freq2[data_str[i]][data_str[i - 1]] = 1
                else:
                    i += 1
                i += 1

            if e and i == data_len:
                if data_str[-1] in freq2['E']:
                    freq2['E'][data_str[-1]] += 1
                else:
                    freq2['E'][data_str[-1]] = 1

    freq1 = {}
    for i in freq2:
        for j in freq2[i]:
            if j in freq1:
                freq1[j] += freq2[i][j]
            else:
                freq1[j] = freq2[i][j]
    for i in freq2:
        for j in freq2[i]:
            freq2[i][j] /= freq1[j]

    try:
        out_file = open("../../statistics/freq2_" + datatype + ('_S' if s else '') + ('_E' if e else '') + ".json", 'w')
        json.dump(freq2, out_file)
        out_file.close()
    finally:
        return freq2


def calc_freq2_pinyin(datatype, s=True, e=True):
    freq2 = {'E_E': {}} if e else {}
    for char, char_pinyin_list in char_pinyin.items():
        for pinyin in char_pinyin_list:
            freq2[char + '_' + pinyin] = {}
    with open("../../resources/" + datatype + "_list.json") as in_file:
        data_list = json.load(in_file)
        in_file.close()
    for data_str in data_list:
        data_len = len(data_str)
        # mark pinyin
        data_pinyin_list = []
        data_pinyin = PY.lazy_pinyin(data_str)
        for i in range(0, data_len):
            if data_str[i] not in char_pinyin:
                data_pinyin[i] = '-'
            elif data_pinyin[i] not in char_pinyin[data_str[i]]:
                data_pinyin[i] = random.choice(char_pinyin[data_str[i]])
            data_pinyin_list.append(data_str[i] + '_' + data_pinyin[i])

        if data_len > 0:
            if s and data_pinyin[0] != '-':
                if 'S_S' in freq2[data_pinyin_list[0]]:
                    freq2[data_pinyin_list[0]]['S_S'] += 1
                else:
                    freq2[data_pinyin_list[0]]['S_S'] = 1

            i = 1
            # iteratively count
            while i < data_len:
                if data_pinyin[i] == '-':
                    i += 2
                elif data_pinyin[i - 1] == '-':
                    i += 1
                else:
                    if data_pinyin_list[i - 1] in freq2[data_pinyin_list[i]]:
                        freq2[data_pinyin_list[i]][data_pinyin_list[i - 1]] += 1
                    else:
                        freq2[data_pinyin_list[i]][data_pinyin_list[i - 1]] = 1
                    i += 1

            if e and i == data_len:
                if data_pinyin_list[i - 1] in freq2['E_E']:
                    freq2['E_E'][data_str[i - 1]] += 1
                else:
                    freq2['E_E'][data_str[i - 1]] = 1

    freq1 = {}
    for i in freq2:
        for j in freq2[i]:
            if j in freq1:
                freq1[j] += freq2[i][j]
            else:
                freq1[j] = freq2[i][j]
    for i in freq2:
        for j in freq2[i]:
            freq2[i][j] /= freq1[j]

    try:
        out_file = open(
            "../../statistics/freq2_pinyin_" + datatype + ('_S' if s else '') + ('_E' if e else '') + ".json", 'w')
        json.dump(freq2, out_file)
        out_file.close()
    finally:
        return freq2


def calc_freq3(datatype, s=True, e=True):
    freq3 = {'E': {}} if e else {}
    for char in char_pinyin.keys():
        freq3[char] = {}
    with open("../../resources/" + datatype + "_list.json") as in_file:
        data_list = json.load(in_file)
        in_file.close()
    for data_str in data_list:
        data_len = len(data_str)
        if data_len > 1:
            if s and data_str[0] in freq3 and data_str[1] in freq3:
                if 'S' + data_str[0] not in freq3[data_str[1]]:
                    freq3[data_str[1]]['S' + data_str[0]] = 1
                else:
                    freq3[data_str[1]]['S' + data_str[0]] += 1

            i = 2

            # iteratively count
            while i < data_len:
                if data_str[i] not in freq3:
                    i += 3
                elif data_str[i - 1] not in freq3:
                    i += 2
                elif data_str[i - 2] not in freq3:
                    i += 1
                else:
                    if data_str[i - 2:i] not in freq3[data_str[i]]:
                        freq3[data_str[i]][data_str[i - 2:i]] = 1
                    else:
                        freq3[data_str[i]][data_str[i - 2:i]] += 1
                    i += 1

            # ending handle
            if e and i == data_len:
                if data_str[-2:] not in freq3['E']:
                    freq3['E'][data_str[-2:]] = 1
                else:
                    freq3['E'][data_str[-2:]] += 1

    freq2 = {}
    for i in freq3:
        for j in freq3[i]:
            if j in freq2:
                freq2[j] += freq3[i][j]
            else:
                freq2[j] = freq3[i][j]
    for i in freq3:
        for j in freq3[i]:
            freq3[i][j] /= freq2[j]

    try:
        out_file = open("../../statistics/freq3_" + datatype + ('_S' if s else '') + ('_E' if e else '') + ".json", 'w')
        json.dump(freq3, out_file)
        out_file.close()
    finally:
        return freq3


def calc_freq3_pinyin(datatype, s=True, e=True):
    PY.load_phrases_dict({'那些': [['nà'], ['xiē']], '哪些': [['nǎ'], ['xiē']], '哪个': [['nǎ'], ['gè']]})
    freq3 = {'E_E': {}} if e else {}
    for char in char_pinyin.keys():
        for pinyin in char_pinyin[char]:
            freq3[char + '_' + pinyin] = {}
    with open("../../resources/" + datatype + "_list.json") as in_file:
        data_list = json.load(in_file)
        in_file.close()
    for data_str in data_list:
        data_len = len(data_str)
        # mark pinyin
        data_pinyin_list = []
        data_pinyin = PY.lazy_pinyin(data_str)
        for i in range(0, data_len):
            if data_str[i] not in char_pinyin:
                data_pinyin[i] = '-'
            elif data_pinyin[i] not in char_pinyin[data_str[i]]:
                data_pinyin[i] = random.choice(char_pinyin[data_str[i]])
            data_pinyin_list.append(data_str[i] + '_' + data_pinyin[i])

        # count frequency
        if data_len > 1:
            # starting item
            if s and data_pinyin_list[0][-1] != '-' and data_pinyin_list[1][-1] != '-':
                prev_str_pinyin = ('S_S ' + data_pinyin_list[0])
                if prev_str_pinyin not in freq3[data_pinyin_list[1]]:
                    freq3[data_pinyin_list[1]][prev_str_pinyin] = 1
                else:
                    freq3[data_pinyin_list[1]][prev_str_pinyin] += 1

            # iteratively count
            i = 2
            while i < data_len:
                if data_pinyin_list[i][-1] == '-':
                    i += 3
                elif data_pinyin_list[i - 1][-1] == '-':
                    i += 2
                elif data_pinyin_list[i - 2][-1] == '-':
                    i += 1
                else:
                    prev_str_pinyin = data_pinyin_list[i - 2] + ' ' + data_pinyin_list[i - 1]
                    if prev_str_pinyin not in freq3[data_pinyin_list[i]]:
                        freq3[data_pinyin_list[i]][prev_str_pinyin] = 1
                    else:
                        freq3[data_pinyin_list[i]][prev_str_pinyin] += 1
                    i += 1

            # ending handle
            if e and i == data_len:  # i == data_len guarantees the last 2 characters are available
                prev_str_pinyin = data_pinyin_list[i - 2] + ' ' + data_pinyin_list[i - 1]
                if prev_str_pinyin not in freq3[('E_E')]:
                    freq3[('E_E')][prev_str_pinyin] = 1
                else:
                    freq3[('E_E')][prev_str_pinyin] += 1

    freq2 = {}
    for i in freq3:
        for j in freq3[i]:
            if j in freq2:
                freq2[j] += freq3[i][j]
            else:
                freq2[j] = freq3[i][j]
    for i in freq3:
        for j in freq3[i]:
            freq3[i][j] /= freq2[j]

    try:
        out_file = open("../../statistics/freq3_pinyin_sentence_S_E.json", 'w')
        json.dump(freq3, out_file)
        out_file.close()
    finally:
        return freq3


if __name__ == "__main__":
    with open("../../resources/char_pinyinList_dict.json") as in_file:
        char_pinyin = json.load(in_file)
        in_file.close()
    # calc_freq1(char_pinyin)
    freq1_pinyin = calc_freq1_pinyin()
    # freq2sentence = calc_freq2('sentence', s=True, e=False)
    # freq2word = calc_freq2('word', s=True, e=True)
    # freq2word = calc_freq2('word', s=False, e=False)
    # freq2sentence_pinyin = calc_freq2_pinyin('sentence', s=True, e=True)
    # freq3sentence = calc_freq3('sentence', s=True, e=True)
    # freq3sentence_pinyin = calc_freq3_pinyin('sentence', s=True, e=True)
