import os.path

from Algorithm.FileUtils import *
from Algorithm.HuffmanCompress import *

def call_HuffmanCompressor(file, output_dir):

    if file is None:
        return "No Files"

    if output_dir is None:
        return "No Output Directory"

    print(file)
    print(output_dir)

    if os.path.isfile(file):
        save_name = os.path.splitext(os.path.basename(file))[0]
    elif os.path.isdir(file):
        save_name = os.path.basename(file)
    else:
        return "Error, file path can not get save name!"

    save_name = save_name + ".myzip"

    prepared_data = prepare_items([file])

    compressed = compress_huffman(prepared_data)
    print("Compressed finish!")

    target_path = os.path.normpath(os.path.join(output_dir, save_name))
    save_file(compressed, target_path)

    return "Save Successful!"

def call_HuffmanDecompressor(myzip_path, output_dir):
    if myzip_path is None:
        return "No Files"
    if output_dir is None:
        return "No Output Directory"

    print(myzip_path)
    print(output_dir)

    zip_data = load_file(myzip_path)
    decompress_huffman(zip_data, output_dir)

    return "Save Successful!"