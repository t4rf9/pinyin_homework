#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'ZX'

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
