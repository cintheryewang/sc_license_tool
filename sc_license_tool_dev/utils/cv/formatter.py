#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
'''
@File    :   formatter.py
@Project :
@Time    :   2023/9/25 9:10
@Author  :   Yifei WANG
@Version :
@python  :   v3.10
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
'''

import re
import warnings

warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import numpy as np
# CV
import cv2 as cv


# =========================== Formatter ===========================
def cv_text(image, text, x, y, s, font=0.5, width=1, color=(255, 255, 255)):
    for i, line in enumerate(text.split('\n')):
        y_ = y + i * s
        cv.putText(image, line, (x, y_), cv.FONT_HERSHEY_SIMPLEX,
                   font, color, width, cv.LINE_AA)


def solid_label(image, base_point, c_x, text, font_scale, thickness, margin=2, color=(0, 0, 0)):
    fontFace = cv.FONT_HERSHEY_SIMPLEX
    # 计算文本的宽高，baseLine
    (width, height), bottom = cv.getTextSize(text, fontFace=fontFace, fontScale=font_scale, thickness=thickness)
    # 计算覆盖文本的矩形框坐标
    left_x = c_x - int(width / 2)
    topleft = (int(left_x - margin), int(base_point[1] + margin))
    bottomright = (c_x + int(width / 2) + margin, base_point[1] + height + margin * 2)
    topleft = (int(topleft[0]), int(topleft[1]))
    bottomright = (int(bottomright[0]), int(bottomright[1]))
    cv.rectangle(image, topleft, bottomright, thickness=-1, color=color)
    # 绘制文本
    cv.putText(image, text, (left_x, base_point[1] + height + margin), fontScale=font_scale, fontFace=fontFace,
               color=(255, 255, 255), thickness=thickness, lineType=cv.LINE_AA)


def solid_label_plt(base_point, c_x, text, font_scale, thickness, margin=2, color='lime'):
    fontFace = cv.FONT_HERSHEY_SIMPLEX
    # 计算文本的宽高，baseLine
    (width, height), bottom = cv.getTextSize(text, fontFace=fontFace, fontScale=font_scale, thickness=thickness)
    # 计算覆盖文本的矩形框坐标
    left_x = c_x - int(width / 2)
    topleft = (left_x - margin, base_point[1] + margin)
    bottomright = (c_x + int(width / 2) + margin, base_point[1] + height + margin * 2)
    ax = plt.gca()
    rec = plt.Rectangle(topleft, width, height, color=color, fill=True)
    ax.add_patch(rec)
    plt.text(left_x, base_point[1] + height + margin, text)

    # cv.rectangle(image, topleft, bottomright, thickness=-1, color=color)
    # 绘制文本
    # cv.putText(image, text, (left_x, base_point[1] + height + margin), fontScale=font_scale, fontFace=fontFace,
    #            color=(255, 255, 255), thickness=thickness, lineType=cv.LINE_AA)


def df_formatter(col, decimal=3, pixel=1.0):
    from collections.abc import Iterable
    rs = len(col)
    result = []
    for r in range(rs):
        if isinstance(col[r], Iterable):
            result.append([np.around(i * pixel, decimal) for i in col[r]])
            # print(col[r],[np.around(i * pixel, decimal) for i in col[r]])
        else:
            result.append(np.around(col[r] * pixel, decimal))
            # print(col[r],np.around(col[r] * pixel, decimal))
    return result
