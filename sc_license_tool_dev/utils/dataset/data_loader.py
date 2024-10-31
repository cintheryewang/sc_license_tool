#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# cython:language_level=3
"""
@File    :   data_loader.py
@Project :
@Time    :   2023/10/18 17:17
@Author  :   Yifei WANG
@Version :   0.1.0(20231018)
@python  :   v3.10.9
@Contact :   mail:yifeiwang@amecnsh.com  tel:3445
@Desc    :
"""

import numpy as np
import pandas as pd
import matplotlib
import os
import re
import time
from PyQt5.QtWidgets import *
matplotlib.use('Qt5Agg')

hrz = "-" * 50


class Folder:
    """
    Traverse files in a folder
    """

    def __init__(self, path=None):
        """
        :param path: customized folder path
        """
        self.folder_path = QFileDialog.getExistingDirectory(None) if path is None else path

    def file_list(self):
        return os.listdir(self.folder_path)

    def file_num(self) -> int:
        return len(self.file_list())

    def folder_sort(self):
        if self.file_num() > 0:
            self.file_list().sort(key=lambda fn: os.path.getmtime(self.folder_path + "\\" + fn))
        else:
            print('! the folder is empty! \n', hrz)

    def file_added(self, num_initial_files=0) -> bool:
        dl_count = self.file_num()
        print('原有 %u 个文件，现有 %u 个文件' % (num_initial_files, dl_count))
        added = True if dl_count > num_initial_files else False
        return added

    def rename_file(self, new_name, old_name=None, filetype='.xml', sort_by_time=True, temp_index=None):
        if sort_by_time:
            self.folder_sort()
        else:
            pass
        old_name = self.file_list()[-1] if old_name is None else old_name
        print('即将修改的文件为：' + old_name)
        if new_name + filetype in self.file_list():
            print('名字叫 %s 的文件已存在了！正在添加时间标记重新命名' % new_name)
            local_time = time.strftime("_%Y-%m-%d_%H-%M", time.localtime(time.time()))
            os.rename(os.path.join(self.folder_path, old_name),
                      os.path.join(self.folder_path, new_name + str(temp_index) + local_time + filetype))
        else:
            os.rename(os.path.join(self.folder_path, old_name),
                      os.path.join(self.folder_path, new_name + str(temp_index) + filetype))
            print('该文件已被重命名为：' + new_name + str(temp_index) + filetype)


def sub_folder_add(path):
    folder_ext = os.path.exists(path)
    if not folder_ext:
        os.makedirs(path)
        print(f'New folder created:\n  {path}')


def magic_data_viewer(path: str, data_file_type: str = 'csv'):
    """
    Quickly grab all files and folders based on parent folder path
    Parameters
    ----------
    path
        parent folder path
    data_file_type
        file type to grab

    Returns
    -------
    2 pandas dataframes of folder paths and file paths
    Examples
    -------
    >>> folders, files, file_stat = yf.magic_data_viewer(path,'csv')
    >>> file_stat
    """
    mat = data_file_type
    folders = [['parent', path]]
    files = []
    for f in folders:
        # print(f)
        folder = Folder(f[1])
        sub_list = folder.file_list()
        for i in sub_list:  # 遍历文件夹元素
            path = folder.folder_path + '/' + i  # 拓展文件夹路径
            find_file = re.search('.*\.\w{1,5}$', i)  # 找后缀
            if find_file is None:  # 没有后缀 = 有文件夹
                # print(f"folder：{i}")
                pre_ = re.search('(?<=/).*$', path).group()
                folders.append([pre_, path])
            elif re.search(f'.*\.{mat}$', i):
                # print(f'file: {find_file.group()}')
                # abbrev = re.search('(?<!\.)\w{7}(?=\.\w{2,4}\.)', i)
                abbrev = re.search('(?<=2023)\w{4}_\w{4}', i)
                if abbrev is not None:
                    abbrev = abbrev.group()
                else:
                    abbrev = i
                files.append([f[0], path, abbrev, folder.folder_path, i])

    folders = pd.DataFrame(folders, columns=['tier', 'path'])
    files = pd.DataFrame(files, columns=['tier', 'path', 'abbrev', 'parent_path', 'file_name'])
    stat = files.pivot_table(index=['tier'], values='path', aggfunc=np.count_nonzero)
    return folders, files, stat


def magic_data_loader(file_df):
    """
    Grab the data based on the results returned by the magic view and store it in the dictionary
    Parameters
    ----------
    file_df

    Returns
    -------
    Examples
    -------
    >>> datas, steps = yf.magic_data_loader(files)
    """
    datas = {}
    step_marks = {}
    print(f'data loaded: \n{hrz}')
    for i in range(len(file_df)):
        data = pd.read_csv(file_df['path'][i], sep="\t").iloc[:, :-4]
        datas[file_df['tier'][i] + '_' + file_df['abbrev'][i]] = data
        print(file_df['tier'][i] + '_' + file_df['abbrev'][i])

        step_mark = []
        for s in range(len(data["StepNumber"])):
            if s > 0 and data["StepNumber"][s] > data["StepNumber"][s - 1]:
                step_mark.append(data.index[s])
        step_marks[file_df['tier'][i] + '_' + file_df['abbrev'][i]] = step_mark
    return datas, step_marks


def magic_data_recipe_finder(file_df):
    recipes = []
    for i in range(len(file_df)):
        raw = pd.read_csv(file_df['path'][i], sep="\t", low_memory=False)
        recipe = raw['Recipe'][0] if 'Recipe' in raw.columns else None
        recipes.append(
            [recipe, file_df['parent_path'][i], file_df['file_name'][i], file_df['abbrev'][i], file_df['path'][i]])
    return pd.DataFrame(recipes, columns=['recipe', 'parent', 'name', 'abbrev', 'path'])


if __name__ == "__main__":
    folders, files, file_stat = magic_data_viewer(
        r"D:\work_zone\data_project_files\data\RUN_DIFF\xingjian_1011\csvs\1006")
    print(files.to_markdown())
    magic_data_recipe_finder(files)
# %%
