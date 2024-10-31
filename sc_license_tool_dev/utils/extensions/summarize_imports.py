import os
import re

def summarize_imports(directory):
    """
    Summarize all imported packages from .py files in the specified directory.

    Parameters
    ----------
    directory : str
        The path to the directory containing .py files.

    Returns
    -------
    list
        A sorted list of unique imported packages.
    """
    import_pattern = re.compile(r'^\s*(?:import|from)\s+([a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)*)')
    imports = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = import_pattern.match(line)
                        if match:
                            imports.add(match.group(1))

    return sorted(imports)

def main():
    directory = input("请输入要扫描的目录路径: ")
    imports = summarize_imports(directory)
    print("导入的包如下:")
    for package in imports:
        print(package)

if __name__ == "__main__":
    main()
