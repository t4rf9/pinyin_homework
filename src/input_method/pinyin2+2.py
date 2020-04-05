#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import sys
import json

with open("../../statistics/freq1char.json") as in_file:
    freq1 = json.load(in_file)
    in_file.close()

with open("../../statistics/freq2char_sentence.json") as in_file:
    freq2_sentence = json.load(in_file)
    in_file.close()

with open("../../resources/pinyin_charList_dict.json") as in_file:
    pinyin_dict = json.load(in_file)
    in_file.close()


def smoothing(p1, p2):
    l = 0.08
    return l * p1 + (1 - l) * p2


def generate_output(pinyin_list, depth):
    global freq1, freq2_sentence, pinyin_dict
    length = len(pinyin_list)

    dp_lists = [[]]
    for curr_char in pinyin_dict[pinyin_list[0]]:
        dp_lists[-1].append((curr_char, smoothing(freq1[curr_char],
                                                  freq2_sentence[curr_char]['S']
                                                  if 'S' in freq2_sentence[curr_char] else 0)))

    for i in range(1, min(depth, length)):
        dp_lists.append([])
        for curr_char in pinyin_dict[pinyin_list[i]]:
            for prev_str, prev_freq in dp_lists[-2]:
                # print("dp_lists[-2]:\t", dp_lists[-2])
                dp_lists[-1].append((prev_str + curr_char,
                                     prev_freq * smoothing(freq1[curr_char], freq2_sentence[curr_char][prev_str[-1]]
                                     if prev_str[-1] in freq2_sentence[curr_char] else 0)))

    for i in range(depth, length):
        dp_lists.append([])
        for curr_char in pinyin_dict[pinyin_list[i]]:
            max_str_freq = ['', 0]
            # print("prev1_str_list:\t", prev1_str_list)
            for prev_str, prev_freq in prev1_str_list:
                # print("prev_str:\t", prev_str)
                curr_freq = prev_freq * smoothing(freq1[curr_char],
                                                  freq2_sentence[curr_char][prev_str[-1]]
                                                  if prev_str[-1] in freq2_sentence[curr_char] else 0)
                if curr_freq > max_str_freq[1]:
                    max_str_freq = [prev_str + curr_char, curr_freq]
            if max_str_freq[0] != '':
                curr_str_list.append(max_str_freq)


        del dp_lists[0]

    for curr_str, curr_freq in curr_str_list:
        curr_freq *= freq2_sentence['E'][curr_str[-1]] if curr_str[-1] in freq2_sentence['E'] else 0

    output = ['', 0]
    for curr in curr_str_list:
        if curr[1] > output[1]:
            output = curr
    return output[0]


def calc_accuracy():
    with open(
            "/Users/linzexi/Documents/THU/Courses/2020-Spring/人工智能导论/Homework/PinYin/data/std_output.txt") as std_outf:
        with open(
                "/Users/linzexi/Documents/THU/Courses/2020-Spring/人工智能导论/Homework/PinYin/data/tmp_output.txt") as tmp_outf:
            total_line = 0
            accurate_line = 0
            total_char = 0
            accurate_char = 0
            std_lines = std_outf.readlines()
            tmp_lines = tmp_outf.readlines()
            tmp_outf.close()
    std_outf.close()

    for i in range(0, len(std_lines)):
        total_line += 1
        flag = True
        for j in range(0, len(std_lines[i]) - 1):
            total_char += 1
            if std_lines[i][j] == tmp_lines[i][j]:
                accurate_char += 1
            else:
                flag = False
        if flag:
            accurate_line += 1
    return accurate_char / total_char, accurate_line / total_line


def main(in_filename, out_filename=''):
    global freq1, freq2_sentence
    with open(in_filename) as input_file:
        in_lines = input_file.readlines()
        input_file.close()

    out_str = ''
    for line in in_lines:
        out_str += generate_output(line.strip().lower().split(), 3) + '\n'

    try:
        output_file = open(out_filename, 'w')
        output_file.write(out_str)
        output_file.close()
    except:
        print(out_str)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    print(calc_accuracy())
