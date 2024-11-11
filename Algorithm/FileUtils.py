import huffman
import os
from pathlib import Path
from bitarray import bitarray

# 读取任意文件为二进制数据
def read_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File not found - {file_path}"
    except IOError as e:
        return f"Error: Could not read file {file_path} - {e}"

# 处理单个文件
def get_single_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            file_content = file.read()
        return {
            "relative_path": os.path.basename(file_path),  # 文件名
            "isDirectory": False,
            "content": file_content
        }
    else:
        raise ValueError("File not found - {}".format(file_path))


def get_single_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError(f"'{folder_path}' is not a valid directory.")

    prepared_data = []

    for root, dirs, files in os.walk(folder_path):
        # 处理目录
        for dir_name in dirs:
            relative_path = os.path.relpath(os.path.join(root, dir_name), folder_path)
            print(f"found dir {relative_path}")  # 调试信息
            prepared_data.append({
                "relative_path": relative_path,
                "isDirectory": True,
                "content": None  # 目录没有内容
            })

        # 处理文件
        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, folder_path)
            print(f"found file {relative_path}")  # 调试信息
            with open(file_path, 'rb') as file:
                file_content = file.read()
            prepared_data.append({
                "relative_path": relative_path,
                "isDirectory": False,
                "content": file_content
            })

    return prepared_data

def prepare_items(input_paths):
    all_prepared_data = []

    for path in input_paths:
        if os.path.isfile(path):
            # 单个文件
            file_data = get_single_file(path)
            all_prepared_data.append(file_data)
        elif os.path.isdir(path):
            # 单个文件夹
            folder_data = get_single_folder(path)
            all_prepared_data.extend(folder_data)
        else:
            print(f"Warning: '{path}' is not a valid file or directory.")

    return all_prepared_data

def verify_prepared_data(prepared_data):
    for item in prepared_data:
        print("========================================")
        print(f"Relative Path: {item['relative_path']}")
        print(f"Is Directory: {item['isDirectory']}")

        if not item['isDirectory']:
            # 如果是文件，检查文件内容的一部分
            content_preview = item['content'][:50]  # 只显示前 50 个字节
            print(f"Content (Preview, 50 bytes max): {content_preview}")
            print(f"Content Length: {len(item['content'])} bytes")
        print("========================================\n")

if __name__ == '__main__':
    path1 = r"C:\Users\77511\Desktop\MyFile\贝尔卡设定文件夹\世界观.txt"
    path2 = r"C:\Users\77511\Desktop\MyFile\同人图\白底.jpg"
    path3 = r"C:\Users\77511\Desktop\MyFile\同人图"
    path4 = r"C:\Users\77511\Desktop\MyFile\作业\m1.2"

    input_paths = [path4]
    prepared_data = prepare_items(input_paths)
    # 验证是否正确读取
    verify_prepared_data(prepared_data)


