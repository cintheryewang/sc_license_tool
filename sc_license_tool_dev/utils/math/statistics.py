#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
'''
@File    :   math.py
@Project :
@Time    :   2023/9/25 9:09
@Author  :   Yifei WANG
@Version :
@python  :   v3.10
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
'''


import warnings
import numpy as np
warnings.filterwarnings('ignore')


# =========================== Statistics ===========================

def mad(x, z_limit=3):
    # Calculate the median of the input array
    med = np.median(x)

    # Compute the absolute deviations from the median
    x_ = np.abs(x - med)

    # Calculate the MAD value
    mad_ = np.median(x_)

    # Calculate the lower and upper bounds based on the z_limit
    lower_bound = med - z_limit * mad_ / 0.6745
    upper_bound = med + z_limit * mad_ / 0.6745

    # Return the median, MAD, and the bounds
    return med, mad_, lower_bound, upper_bound


def mode(numbers):
    unique_nums = np.unique(numbers)
    counts = np.bincount(numbers)
    mode_num = unique_nums[np.argmax(counts)]
    return mode_num


def get_int(data):
    iterable = hasattr(data, '__iter__')
    if iterable:
        data_ = data.copy()
        for d in range(len(data)):
            data_[d] = int(round(data[d], 0))
        return data_
    else:
        return int(round(data, 0))
