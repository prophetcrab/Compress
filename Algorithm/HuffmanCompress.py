import huffman
import pickle
from pympler import asizeof
from bitarray import bitarray

from Algorithm.FileUtils import *


def compress_huffman(prepared_data):
    compressed_data = []

    for item in prepared_data:
        if item["isDirectory"]:
            # 对于目录，只保留路径和目录标识
            compressed_data.append({
                "relative_path": item["relative_path"],
                "isDirectory": True
            })
        else:
            file_content = item["content"]
            encoded, codes = huffman.encode(list(file_content))

            encoded_array = bitarray()
            encoded_array.extend(encoded)



            compressed_data.append({
                "relative_path": item["relative_path"],
                "isDirectory": False,
                "originalSize": len(file_content),
                "encodedData": encoded_array,
                "huffmanCodes": codes,
            })

            print(f"file_content Size: {asizeof.asizeof(file_content) / 1024 / 1024} Mbytes")
            print(f"encoded Size: {asizeof.asizeof(encoded_array) / 1024 / 1024} Mbytes")

    return compressed_data

def decompress_huffman(compressed_data, output_path):
    for entry in compressed_data:
        full_path = os.path.join(output_path, entry["relative_path"])

        if entry["isDirectory"]:
            # 创建目录
            os.makedirs(full_path, exist_ok=True)
            print(f"Created directory: {full_path}")
        else:
            decode_map = huffman.generate_decode_map(entry["huffmanCodes"])
            encoded_bits = entry["encodedData"].to01()
            decoded = huffman.decode(decode_map, encoded_bits)
            file_content = bytes(decoded)

            # 确保父目录存在
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # 写入解压后的文件
            with open(full_path, 'wb') as file:
                file.write(file_content)
            print(f"Restored file: {full_path}")

    print(f"Decompressed data has been restored to '{output_path}'")

def save_file(compressed_data, output_file):
    with open(output_file, 'wb') as file:
        pickle.dump(compressed_data, file)
    print(f"Compressed data saved to '{output_file}'")

def load_file(input_file):
    with open(input_file, 'rb') as file:
        compressed_data = pickle.load(file)
    return compressed_data


if __name__ == '__main__':
    path1 = r"C:\Users\77511\Desktop\MyFile\贝尔卡设定文件夹\世界观.txt"

    output_path = r"D:\PythonProject2\Compress\Output"
    save_name = "Output.myzip"

    prepared_data = prepare_items([path1])
    compressed = compress_huffman(prepared_data)

    save_file(compressed, os.path.join(output_path, save_name))
    zip_data = load_file(os.path.join(output_path, save_name))

    decompress_huffman(zip_data, output_path)