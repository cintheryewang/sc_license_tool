#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   exception_handeler.py
@Project :
@Time    :   2024/1/11 11:28
@Author  :   Yifei WANG
@Version :
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
"""

import functools
import traceback
from SEMIR.utils.log import get_logger

logger = get_logger(__name__)


def catch_and_log(func):
    """A decorator that catches and logs exceptions in a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 获取错误堆栈信息
            tb = traceback.format_exc()
            # 过滤掉与装饰器相关的堆栈信息
            filtered_tb = '\n'.join([line for line in tb.splitlines() if "wrapper" not in line])
            logger.error(f"Exception occurred in function {func.__name__}\n{filtered_tb}")
            # 可以选择重新抛出异常或返回一个错误值
            # raise  # 可选：重新抛出异常
            return -1  # 或返回特定的值

    return wrapper


if __name__ == '__main__':
    # Example usage
    @catch_and_log
    def divide(x, y):
        return x / y


    print(divide(10, 0))  # 这将导致除以零的异常，但不会使程序崩溃
