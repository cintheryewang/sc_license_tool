#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   ir_tools.py
@Project :
@Time    :   2023/9/25 8:55
@Author  :   Yifei WANG
@Version :
@python  :   v3.10
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
"""

import re
import numpy as np
import cv2 as cv
import datetime
import warnings
from tkinter import filedialog

from SEMIR.utils import data_loader

warnings.filterwarnings('ignore')


# =========================== Image Import & Export ===========================

def image_load(image_path=None):
    try:
        if image_path is not None:
            image = cv.imread(image_path)
            # logger.info(f'image from {image_path} imported')
        else:
            image_path = filedialog.askopenfilename()
            image = cv.imread(image_path)
        return image
    except Exception as e:
        pass
        # logger.error(f'image from {image_path} NOT imported')
        # logger.error(f'{e}')


def image_save(image: np.array, name: str, save_folder_path=None):
    path = save_folder_path if save_folder_path else filedialog.asksaveasfilename()
    f_list = data_loader.Folder(path).file_list()
    pattern = re.compile(f"{name}.[(jpe?g)(png)]")
    exist = list(filter(pattern.match, f_list))
    if exist:
        # logger.warning(f"image {name} same name file exists")
        time_now = datetime.datetime.now().strftime("-%m-%d-%H-%M")
        name = name + time_now
    cv.imwrite(path + "/" + name + ".png", image,
               [int(cv.IMWRITE_PNG_COMPRESSION), 100])
    # logger.info(f"image {name} saved as {path}/{name}.png")


def pix_size_extractor_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            pix = re.search('(?<=PixelSize=)\d+\.\d+', l, re.I)
            if pix:
                pix = float(pix.group())
                return pix
