#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

"""
When given a input file which contains lines of pinyin inputs 
and the corresponding lines Chinese outputs in the same order,
this script separates pinyin lines and Chinese lines and save them in two .txt files,
i.e. ../../data/std_input.txt and ../../data/std_output.txt ,
for the convenience of inputting and result analysis.
"""

with open("../../data/std_input_origin.txt") as origin:
    with open("../../data/std_input.txt", 'w') as std_input:
        with open("../../data/std_output.txt", 'w') as std_output:
            for line in origin.readlines():
                if line.isascii():
                    std_input.write(line.strip() + '\n')
                else:
                    std_output.write(line.strip() + '\n')
            std_output.close()
        std_input.close()
    origin.close()
