#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import sys
import json


def smoothing2(p1, p2):
    l1 = 0.08
    return l1 * p1 + (1 - l1) * p2


def smoothing3(p1, p2, p3):
    # sentence  s e
    #                   l1 = 5e-5, l2 = 0.12, 0.8657, 0.5181
    #                   l1 = 5e-50, l2 = 0.12, 0.8736, 0.5292
    #                   l1 = 1e-50, l2 = 0.86, 0.8775, 0.5460

    l1 = 1e-30
    l2 = 0.86
    return l1 * p1 + l2 * p2 + (1 - l1 - l2) * p3


def generate_output(pinyin_list, freq1, freq2, freq3, pinyin_dict):
    length = len(pinyin_list)

    curr_str_pinyin_freq_list = []
    for curr_char in pinyin_dict[pinyin_list[0]]:
        curr_char_pinyin = curr_char + '_' + pinyin_list[0]
        curr_str_pinyin_freq_list.append([
            ['S_S', curr_char_pinyin],
            smoothing2(freq1[curr_char_pinyin],
                       freq2[curr_char_pinyin]['S_S'] if 'S_S' in freq2[curr_char_pinyin] else 0)
        ])

    prev_str_pinyin_freq_list = curr_str_pinyin_freq_list.copy()
    curr_str_pinyin_freq_list = []
    for curr_char in pinyin_dict[pinyin_list[1]]:
        curr_char_pinyin = curr_char + '_' + pinyin_list[1]
        max_str_freq = [[], 0]
        for prev_str_pinyin_list, prev_freq in prev_str_pinyin_freq_list:
            # print("prev_str_pinyin_list:\t", prev_str_pinyin_list)
            prev_str_pinyin2 = prev_str_pinyin_list[-2] + ' ' + prev_str_pinyin_list[-1]
            curr_freq = \
                prev_freq * \
                smoothing3(freq1[curr_char_pinyin],
                           (freq2[curr_char_pinyin][prev_str_pinyin_list[-1]] *
                            freq2[prev_str_pinyin_list[-1]][prev_str_pinyin_list[-2]])
                           if prev_str_pinyin_list[-1] in freq2[curr_char_pinyin]
                              and prev_str_pinyin_list[-2] in freq2[prev_str_pinyin_list[-1]] else 0,
                           freq3[curr_char_pinyin][prev_str_pinyin2]
                           if prev_str_pinyin2 in freq3[curr_char_pinyin] else 0
                           )
            if curr_freq > max_str_freq[1]:
                max_str_freq = [prev_str_pinyin_list + [curr_char_pinyin], curr_freq]

        if max_str_freq[0]:
            curr_str_pinyin_freq_list.append(max_str_freq)

    for i in range(2, length):
        prev_str_pinyin_freq_list = curr_str_pinyin_freq_list.copy()
        curr_str_pinyin_freq_list = []
        # print(pinyin_list)
        for curr_char in pinyin_dict[pinyin_list[i]]:
            curr_char_pinyin = curr_char + '_' + pinyin_list[i]
            max_str_freq = [[], 0]
            # print("prev1_str_list:\t", prev1_str_list)
            for prev_str_pinyin_list, prev_freq in prev_str_pinyin_freq_list:
                # print("prev_str:\t", prev_str)
                prev_str_pinyin2 = prev_str_pinyin_list[-2] + ' ' + prev_str_pinyin_list[-1]
                curr_freq = \
                    prev_freq * \
                    smoothing3(freq1[curr_char_pinyin],
                               (freq2[curr_char_pinyin][prev_str_pinyin_list[-1]] *
                                freq2[prev_str_pinyin_list[-1]][prev_str_pinyin_list[-2]])
                               if prev_str_pinyin_list[-1] in freq2[curr_char_pinyin]
                                  and prev_str_pinyin_list[-2] in freq2[prev_str_pinyin_list[-1]]
                               else 0,
                               freq3[curr_char_pinyin][prev_str_pinyin2]
                               if prev_str_pinyin2 in freq3[curr_char_pinyin] else 0
                               )
                if curr_freq > max_str_freq[1]:
                    max_str_freq = [prev_str_pinyin_list + [curr_char_pinyin], curr_freq]
            if max_str_freq[0]:
                curr_str_pinyin_freq_list.append(max_str_freq)

    for curr_str_pinyin_list, curr_freq in curr_str_pinyin_freq_list:
        curr_str_pinyin2 = curr_str_pinyin_list[-2] + ' ' + curr_str_pinyin_list[-1]
        curr_freq *= \
            smoothing3(
                1,
                (freq2['E_E'][curr_str_pinyin_list[-1]] *
                 freq2[curr_str_pinyin_list[-1]][curr_str_pinyin_list[-2]])
                if curr_str_pinyin_list[-1] in freq2['E_E']
                   and curr_str_pinyin_list[-2] in freq2[curr_str_pinyin_list[-1]]
                else 0,
                freq3['E_E'][curr_str_pinyin2]
                if curr_str_pinyin2 in freq3['E_E'] else 0
            )

    output_str_pinyin_list = [[], 0]
    for curr_str_pinyin_list, curr_freq in curr_str_pinyin_freq_list:
        if curr_freq > output_str_pinyin_list[1]:
            output_str_pinyin_list = [curr_str_pinyin_list, curr_freq]

    output_str = ''
    for char_pinyin in output_str_pinyin_list[0][1:]:
        output_str += char_pinyin[0]
    return output_str


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


def main(in_filename, out_filename='', stdout_filename=''):
    with open("../../statistics/freq1_pinyin.json") as freq1_file:
        freq1 = json.load(freq1_file)
        freq1_file.close()

    with open("../../statistics/freq2_pinyin_sentence_S_E.json") \
            as freq2_file:
        freq2 = json.load(freq2_file)
        freq2_file.close()

    with open("../../statistics/freq3_pinyin_sentence_S_E.json") \
            as freq3_file:
        freq3 = json.load(freq3_file)
        freq3_file.close()

    with open("../../resources/pinyin_charList_dict.json") as pinyin_dict_file:
        pinyin_dict = json.load(pinyin_dict_file)
        pinyin_dict_file.close()

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

    with open(out_filename, 'w') as output_file:
        output_file.write(out_str)
        output_file.close()
        if stdout_filename != '':
            print(calc_accuracy(stdout_filename, out_filename))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
