#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   code_assist_1_0_0.py
@Project :
@Time    :   2024/5/16 上午9:53
@Author  :   Yifei WANG
@Version :
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
"""


import pyperclip


def comment_separator(text="func", symbol="=", total_length=80):
    """
    Generate a comment separator with text centered, surrounded by a specified symbol.

    Args:
    symbol (str): The symbol to use for the separator.
    text (str): The text to center within the separator.
    total_length (int): The total length of the separator line.

    Returns:
    str: The formatted separator line.

    Example:
    comment_separator('正弦优化')
    """
    # 首先检查总长度是否足以至少放下文字加两边的空格和至少两个符号
    min_length = len(text) + 2 + 2  # 文本长度 + 两侧空格 + 至少每侧一个符号
    if total_length < min_length:
        return "Error: Total length too short to create a proper separator."

    # 计算两边符号的总空间
    space_for_symbols = total_length - len(text) - 2  # 总长度减去文字和两个空格

    # 分配两边的符号
    symbols_each_side = space_for_symbols // 2

    # 构造分隔符
    left_symbols = symbol * symbols_each_side
    right_symbols = symbol * (space_for_symbols - symbols_each_side)  # 保证如果符号数是奇数，右边多一个

    # 构造完整的分隔符行
    separator_line = f"# {left_symbols} {text} {right_symbols}"
    pyperclip.copy(separator_line)
    print(separator_line)
    print("separator_line copied to clipboard!")


