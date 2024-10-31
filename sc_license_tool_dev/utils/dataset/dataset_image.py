#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   data_set.py
@Project :
@Time    :   2024/6/27 上午9:23
@Author  :   Yifei WANG
@Version :
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
"""

import os
import cv2 as cv
import numpy as np
import h5py
import re
from SEMIR_v2.utils.dataset import dm3_lib as dm3
from matplotlib import pyplot as plt


class ImageDataset:
    def __init__(self, image_paths):
        """
        初始化图像数据集。

        参数:
            image_paths (list): 图像文件路径列表。
        """
        self.image_paths = image_paths

    def __len__(self):
        """
        返回数据集中的图像总数。

        返回:
            int: 数据集的长度。
        """
        return len(self.image_paths)

    def __getitem__(self, idx):
        """
        根据索引获取图像和像素大小。

        参数:
            idx (int): 图像的索引。

        返回:
            tuple: 包含图像和像素大小的元组。
        """
        if idx < 0 or idx >= len(self.image_paths):
            raise IndexError("索引超出范围")

        image_path = self.image_paths[idx]
        image, pix_size = self.load_image(image_path)
        return image, pix_size

    def load_image(self, path):
        """
        从文件路径加载图像的方法，并返回像素大小。

        参数:
            path (str): 图像文件的路径。

        返回:
            tuple: 包含图像和像素大小的元组。
        """
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.tif', '.tiff']:
            image = cv.imread(path)
            if image is None:
                raise FileNotFoundError(f"无法加载图像: {path}")
            pix_size = self.pix_size_extractor_txt(path)
            return image, pix_size
        elif ext == '.dm3':
            return self.decode_dm3(path)
        elif ext == '.emd':
            img_dark, pix_size = self.load_emd(path)
            return img_dark, pix_size
        else:
            raise ValueError(f"不支持的文件格式: {ext}")

    def decode_dm3(self, path):
        """
        解码 dm3 文件，并返回图像和像素大小。

        参数:
            path (str): dm3 文件路径。

        返回:
            tuple: 包含解码后的图像和像素大小的元组。
        """
        dm3f = dm3.DM3(path)
        pix_size = dm3f.pxsize
        A = dm3f.imagedata
        cuts = dm3f.cuts
        A_norm = A.copy()
        if cuts[0] != cuts[1]:
            A_norm[(A <= min(cuts))] = float(min(cuts))
            A_norm[(A >= max(cuts))] = float(max(cuts))
        A_norm = (A_norm - np.min(A_norm)) / (np.max(A_norm) - np.min(A_norm))
        A_norm = np.uint8(np.round(A_norm * 255))
        return A_norm, pix_size[0]

    def load_emd(self, path):
        """
        加载 emd 文件，并返回暗背景图像和像素大小。

        参数:
            path (str): emd 文件路径。

        返回:
            tuple: 包含暗背景图像和像素大小的元组。
        """
        f = h5py.File(path, 'r')
        img_id_0 = list(f["Data/Image"].keys())[0]
        img_id_1 = list(f["Data/Image"].keys())[1]
        img_0 = f[f"Data/Image/{img_id_0}/Data"]
        img_1 = f[f"Data/Image/{img_id_1}/Data"]

        if self.dark_background_divider(img_0[:, :, 0]):
            img_dark = img_0
            img_bright = img_1
        else:
            img_dark = img_1
            img_bright = img_0

        # pix_size = f["Data/Image/{}/PixelSize".format(img_id_0)][()]
        pix_size = None
        return np.array(img_dark), pix_size

    def pix_size_extractor_txt(self, path):
        """
        从文本文件中提取像素大小。

        参数:
            path (str): 文本文件路径。

        返回:
            float: 像素大小。
        """
        txt_path = os.path.splitext(path)[0] + '.txt'
        if not os.path.exists(txt_path):
            return None

        with open(txt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for l in lines:
                pix = re.search('(?<=PixelSize=)\d+\.\d+', l, re.I)
                if pix:
                    return float(pix.group())
        return None

    def dark_background_divider(self, img):
        # 计算直方图
        hist, bins = np.histogram(img, bins=256)
        # plt.plot(hist, color='gray')

        # 计算直方图的左偏和右偏性质
        left_skewness = np.sum(hist[:128]) / np.sum(hist)
        right_skewness = np.sum(hist[128:]) / np.sum(hist)

        # 设置阈值，可以根据需要调整
        skewness_threshold = 0.7

        # 根据左偏和右偏性质判断明暗背景
        if left_skewness > skewness_threshold:
            return True  # Dark background
        elif right_skewness > skewness_threshold:
            return False  # Bright background
        else:
            return None


if __name__ == '__main__':
    from SEMIR_v2.utils.dataset import file_viewer
    import matplotlib

    matplotlib.use('Qt5Agg')
    # path = r"D:\work_zone\data_project_files\data\SEM_TEM\ETCH\ROUNDNESS&TILTING\314M"
    # path = r"D:\work_zone\data_project_files\data\SEM_TEM\ETCH\ROUNDNESS&TILTING\Calculation"
    # path = r"D:\work_zone\data_project_files\data\SEM_TEM\ETCH\ROUNDNESS&TILTING\FIB"
    # path = r"C:\Users\yifeiwang\Desktop\CCP\FIB"
    path = r"D:\work_zone\data_project_files\development\projects\ir\etch\SEMIR_v2\SEMIR_v2\utils\dataset\test_data"
    folders, files, file_stat = file_viewer.magic_data_viewer(path, ['dm3', "tif", "jpg", "emd"])

    # 使用示例
    image_paths = files['path']
    dataset = ImageDataset(image_paths)

    # 获取数据集长度
    print(f"数据集长度: {len(dataset)}")

    # 访问图像
    for idx in range(len(dataset)):
        image, pix_size = dataset[idx]
        print(f"索引 {idx} 的图像尺寸: {image.shape}，像素大小: {pix_size}")
        plt.figure()
        plt.imshow(image)
        plt.show()
