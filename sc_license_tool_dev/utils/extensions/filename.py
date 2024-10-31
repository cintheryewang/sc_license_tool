import os


def list_subfolders(directory):
    """
    List and print all subfolders in the given directory.

    Parameters
    ----------
    directory : str
        The path of the directory to list subfolders from.
    """
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            print(item)


def count_files_in_subfolders(directory):
    """
    Count and print the number of files in each subfolder of the given directory.

    Parameters
    ----------
    directory : str
        The path of the directory to list subfolders from.
    """
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            file_count = len([f for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f))])
            print(f"Folder: {item}, Number of files: {file_count}")


# 示例用法
directory_path = r'\\fileserver\Public\xhk_cell_share_with_simulation\all'
list_subfolders(directory_path)
count_files_in_subfolders(directory_path)
