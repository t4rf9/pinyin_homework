#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

"""
This script generates the Chinese output from pinyin input
based on the model of 3-character dependency
without the consideration of heteronyms
by the greedy algorithm.
"""

import sys
import json
import time


def smoothing2(p1, p2):
    l1 = 0.08
    return l1 * p1 + (1 - l1) * p2


def smoothing3(p1, p2, p3):
    l1 = 0.05
    l2 = 0.20
    return l1 * p1 + l2 * p2 + (1 - l1 - l2) * p3


# return a Chinese string according to the pinyin_list input
# pinyin_list: a list of the input pinyin string
# freq1, freq2, freq3: the relative frequency of 1, 2, 3-character dependency model
# pinyin_dict: the dictionary with pinyin as its keys and lists of Chinese characters as its values
def generate_output(pinyin_list, freq1, freq2, freq3, pinyin_dict):
    length = len(pinyin_list)

    # the list of strings with the highest probability of appearance (with all previous characters fixed)
    # which end with each Chinese character that match the current pinyin,
    # and the probability
    curr_str_list = []

    # the first Chinese character
    for curr_char in pinyin_dict[pinyin_list[0]]:
        curr_str_list.append([
            'S' + curr_char,
            smoothing2(freq1[curr_char], freq2[curr_char]['S'] if 'S' in freq2[curr_char] else 0)
        ])

    # the second Chinese character
    prev_str_list = curr_str_list
    curr_str_list = []
    for curr_char in pinyin_dict[pinyin_list[1]]:
        max_str_freq = ['', 0]
        for prev_str, prev_freq in prev_str_list:
            curr_freq = prev_freq * smoothing3(freq1[curr_char],
                                               freq2[curr_char][prev_str[-1]]
                                               if prev_str[-1] in freq2[curr_char] else 0,
                                               freq3[curr_char][prev_str] if prev_str in freq3[curr_char]
                                               else 0
                                               )
            if curr_freq > max_str_freq[1]:
                max_str_freq = [prev_str + curr_char, curr_freq]

        if max_str_freq[0] != '':
            curr_str_list.append(max_str_freq)

    # the following Chinese characters
    for i in range(2, length):
        prev_str_list = curr_str_list.copy()
        curr_str_list = []
        for curr_char in pinyin_dict[pinyin_list[i]]:
            max_str_freq = ['', 0]
            for prev_str, prev_freq in prev_str_list:
                curr_freq = prev_freq * \
                            smoothing3(freq1[curr_char],
                                       freq2[curr_char][prev_str[-1]]
                                       if prev_str[-1] in freq2[curr_char] else 0,
                                       freq3[curr_char][prev_str[-2:]]
                                       if prev_str[-2:] in freq3[curr_char] else 0
                                       )
                if curr_freq > max_str_freq[1]:
                    max_str_freq = [prev_str + curr_char, curr_freq]
            if max_str_freq[0] != '':
                curr_str_list.append(max_str_freq)

    # the ending empty character
    for curr_str, curr_freq in curr_str_list:
        curr_freq *= smoothing3(1,
                                freq2['E'][curr_str[-1]]
                                if curr_str[-1] in freq2['E'] else 0,
                                freq3['E'][curr_str[-2:]]
                                if curr_str[-2:] in freq3['E'] else 0
                                )

    # output the result string by greedy algorithm
    output = ['', 0]
    for curr in curr_str_list:
        if curr[1] > output[1]:
            output = curr
    return output[0][1:]


# compare the standard output file and the real output file for accuracy
def calc_accuracy(stdout_filename, out_filename):
    with open(stdout_filename) as std_out_file:
        with open(out_filename) as out_file:
            total_line = 0
            accurate_line = 0
            total_char = 0
            accurate_char = 0
            std_lines = std_out_file.readlines()
            tmp_lines = out_file.readlines()
            out_file.close()
        std_out_file.close()

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


def main(in_filename, out_filename='', stdout_filename='', count_method='sentence'):
    startTime = time.process_time()
    with open("../../statistics/freq1.json") as freq1_file:
        freq1 = json.load(freq1_file)
        freq1_file.close()

    with open("../../statistics/freq2_" + count_method + "_S_E.json") \
            as freq2_file:
        freq2 = json.load(freq2_file)
        freq2_file.close()

    with open("../../statistics/freq3_" + count_method + "_S_E.json") \
            as freq3_file:
        freq3 = json.load(freq3_file)
        freq3_file.close()

    with open("../../resources/pinyin_charList_dict.json") as pinyin_dict_file:
        pinyin_dict = json.load(pinyin_dict_file)
        pinyin_dict_file.close()

    print("Load statistics data:\t", time.process_time() - startTime, " s")

    with open(in_filename) as input_file:
        in_lines = input_file.readlines()
        input_file.close()

    out_str = ''
    for line in in_lines:
        line_list = line.strip().lower().split()
        for i in range(0, len(line_list)):
            if line_list[i] == 'lue':
                line_list[i] = 'lve'
            elif line_list[i] == 'nue':
                line_list[i] = 'nve'

        out_str += generate_output(line_list, freq1, freq2, freq3, pinyin_dict) + '\n'

    try:
        output_file = open(out_filename, 'w')
        output_file.write(out_str)
        output_file.close()
        if stdout_filename != '':
            accuracy = calc_accuracy(stdout_filename, out_filename)
            print("Accuracy:\n\tCharacter:\t", accuracy[0], ",\tLine:\t", accuracy[1], "\n")
    except:
        print(out_str)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: ", sys.argv[0], " input_file (output_file) (std_output_file)\n")
