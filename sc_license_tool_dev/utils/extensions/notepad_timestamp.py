#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   notepad_timestamp.py
@Project :
@Time    :   2024/4/7 9:12
@Author  :   Yifei WANG
@Version :
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
"""


import time

def add_timestamp():
    editor.beginUndoAction()
    current_time = time.strftime("[%Y-%m-%d %H:%M:%S] ", time.localtime())
    line_count = editor.getLineCount()
    for line in range(0, line_count):
        editor.insertText(editor.positionFromLine(line), current_time)
    editor.endUndoAction()

add_timestamp()
