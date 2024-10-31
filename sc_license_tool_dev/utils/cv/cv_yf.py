#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   cv_yf.py
@Project :
@Time    :   2023/11/7 15:39
@Author  :   Yifei WANG
@Version :
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
"""


import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

from SEMIR.algorithms.lib.formatter import cv_text


# from SEMIR.log import logger



def image_show_cv(image: np.array, name: str = 'image', wait=0):
    """
    Show images in cv window
    Parameters
    ----------
    image: np.Array
        loaded image
    name: str
        the name of the image
    wait: int, default 0
        cv param, determines the time last of the window

    Returns
    -------
    None
    """
    cv.namedWindow(name, cv.WINDOW_AUTOSIZE)
    cv.imshow(name, image)
    cv.waitKey(wait)
    cv.destroyAllWindows()


def image_show_plt(image: np.array, name: str = 'image', show=False, **kwargs):
    """
    show images in matplotlib window
    Parameters
    ----------
    image: np.Array
        loaded image
    name: str
        the name of the image
    show: bool
        whether to use plt.show(), set to False if runs in ipython
    kwargs
        other params of plt.imshow()
    Returns
    -------
    None
    """
    mat = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    plt.imshow(mat, **kwargs)
    plt.title(name)
    plt.tight_layout()
    if show:
        plt.show()


# =========================== Copyright & Encryption ===========================

def watermark_add(mark_text, image: np.array, img_id):
    r, c = image.shape[:2]
    t1 = np.ones((r, c), dtype=np.uint8) * 254
    lsb0 = cv.bitwise_and(image, t1)
    mark = np.zeros((r, c), dtype=np.uint8)
    cv_text(mark, mark_text, int(c * 0.1), int(r * 0.4), int(r * 0.06), font=c / 1000, width=1)
    wt = mark.copy()
    wt[mark > 0] = 1
    wo = cv.bitwise_or(lsb0, wt)
    # logger.debug(f'{img_id} copyright encrypted')
    return wo


def watermark_extract(image: np.array):
    r, c = image.shape
    t2 = np.ones((r, c), dtype=np.uint8)
    ewb = cv.bitwise_and(image, t2)
    ew = ewb
    ew[ewb > 0] = 255
    return ew
