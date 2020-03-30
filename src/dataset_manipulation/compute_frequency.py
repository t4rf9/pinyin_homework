#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import json

with open("../../resources/char_pinyinList_dict.json") as in_file:
    char_pinyin = json.load(in_file)
    in_file.close()

with open("../../resources/pinyin_charList_dict.json") as in_file:
    pinyin_char = json.load(in_file)
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
    with open("../../statistics/freq1char.json", 'w') as out_file:
        json.dump(freq1char, out_file)
        out_file.close()


def calc_freq2char_by_sentence():
    global char_pinyin, pinyin_char
    freq2char_sentence = {}
    for char in char_pinyin.keys():
        freq2char_sentence[char] = {}
    with open("../../resources/sentence_list.json") as in_file:
        sentence_list = json.load(in_file)
        in_file.close()
    for sentence in sentence_list:
        for i in range(0, len(sentence) - 1):
            if sentence[i] in freq2char_sentence and sentence[i + 1] in freq2char_sentence:
                if sentence[i] in freq2char_sentence[sentence[i + 1]]:
                    freq2char_sentence[sentence[i + 1]][sentence[i]] += 1
                else:
                    freq2char_sentence[sentence[i + 1]][sentence[i]] = 1

    with open("../../statistics/freq2char_sentence.json", 'w') as out_file:
        json.dump(freq2char_sentence, out_file)
        out_file.close()


def calc_freq2char_by_word():
    global char_pinyin, pinyin_char
    freq2char_word = {}
    for char in char_pinyin.keys():
        freq2char_word[char] = {}
    with open("../../resources/word_list.json") as in_file:
        word_list = json.load(in_file)
        in_file.close()
    for word in word_list:
        word_len = len(word)
        i = 1
        while i < word_len and word[i - 1] not in freq2char_word:
            i += 1
        while i < word_len:
            if word[i] in freq2char_word:
                if word[i - 1] in freq2char_word[word[i]]:
                    freq2char_word[word[i]][word[i - 1]] += 1
                else:
                    freq2char_word[word[i]][word[i - 1]] = 1
            else:
                i += 1
            i += 1

    with open("../../statistics/freq2char_word.json", 'w') as out_file:
        json.dump(freq2char_word, out_file)
        out_file.close()


if __name__ == "__main__":
    # calc_freq1char()
    # calc_freq2char_by_sentence()
    calc_freq2char_by_word()
