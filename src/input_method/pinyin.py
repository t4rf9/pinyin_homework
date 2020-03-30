#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

import sys
import json


def main(in_filename, out_filename=''):
    with open("../../resources/pinyin_charList_dict.json") as pinyin_file:
        pinyin_dict = json.load(pinyin_file)
        pinyin_file.close()

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
