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


def main(in_filename, out_filename=''):
    global freq1, freq2_sentence
    with open(in_filename) as input_file:
        in_lines = input_file.readlines()
        input_file.close()

    out_str = ''
    for line in in_lines:
        pinyin_strs = line.strip().split(' ')
        for pinyin in pinyin_strs:
            out_str += pinyin_dict[pinyin][0] if pinyin in pinyin_dict else '?'
        out_str += '\n'

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
