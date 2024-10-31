import os
import re
import time
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QFileDialog


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
            self.file_list().sort(key=lambda fn: os.path.getmtime(os.path.join(self.folder_path, fn)))
        else:
            print('! the folder is empty! \n')

    def file_added(self, num_initial_files=0) -> bool:
        dl_count = self.file_num()
        print('原有 %u 个文件，现有 %u 个文件' % (num_initial_files, dl_count))
        return dl_count > num_initial_files

    def rename_file(self, new_name, old_name=None, filetype='.xml', sort_by_time=True, temp_index=None):
        if sort_by_time:
            self.folder_sort()

        old_name = self.file_list()[-1] if old_name is None else old_name
        print('即将修改的文件为：' + old_name)

        if new_name + filetype in self.file_list():
            print('名字叫 %s 的文件已存在了！正在添加时间标记重新命名' % new_name)
            local_time = time.strftime("_%Y-%m-%d_%H-%M", time.localtime(time.time()))
            new_filename = f"{new_name}{temp_index}{local_time}{filetype}"
        else:
            new_filename = f"{new_name}{temp_index}{filetype}"

        os.rename(os.path.join(self.folder_path, old_name), os.path.join(self.folder_path, new_filename))
        print('该文件已被重命名为：' + new_filename)


def sub_folder_add(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f'New folder created:\n  {path}')


def magic_data_viewer(path: str, data_file_types: list = ['csv']):
    """
    Quickly grab all files and folders based on parent folder path

    Parameters
    ----------
    path : str
        parent folder path
    data_file_types : list
        file types to grab

    Returns
    -------
    folders : pandas.DataFrame
        DataFrame of folder paths
    files : pandas.DataFrame
        DataFrame of file paths
    stat : pandas.DataFrame
        DataFrame of file statistics by tier

    Examples
    --------
    >>> folders, files, file_stat = magic_data_viewer(path, ['csv', 'txt'])
    >>> file_stat
    """
    folders = [['parent', path]]
    files = []
    pattern = re.compile(r'.*\.(?:' + '|'.join(data_file_types) + r')$')

    for f in folders:
        folder = Folder(f[1])
        sub_list = folder.file_list()
        for i in sub_list:
            sub_path = os.path.join(folder.folder_path, i)
            if os.path.isdir(sub_path):
                pre_ = re.search('(?<=/).*$', sub_path).group()
                folders.append([pre_, sub_path])
            elif pattern.match(i):
                abbrev = re.search(r'(?<=2023)\w{4}_\w{4}', i)
                abbrev = abbrev.group() if abbrev else i
                files.append([f[0], sub_path, abbrev, folder.folder_path, i])

    folders_df = pd.DataFrame(folders, columns=['tier', 'path'])
    files_df = pd.DataFrame(files, columns=['tier', 'path', 'abbrev', 'parent_path', 'file_name'])
    stat_df = files_df.pivot_table(index=['tier'], values='path', aggfunc=np.count_nonzero)
    return folders_df, files_df, stat_df


if __name__ == '__main__':
    path = 'your/folder/path'
    folders, files, file_stat = magic_data_viewer(path, ['csv', 'txt'])
    print(file_stat)
