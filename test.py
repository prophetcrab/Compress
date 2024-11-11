import huffman
from pympler import asizeof
from Algorithm.FileUtils import *
from bitarray import bitarray


path = r"C:\Users\77511\Desktop\MyFile\贝尔卡设定文件夹\世界观.txt"
# 编码数据

data = read_file(path)

encoded, codes = huffman.encode(list(data))
decode_map = huffman.generate_decode_map(codes)

# 解码
decoded = huffman.decode(decode_map, encoded)
decoded_data = bytes(decoded)

# 使用 bitarray 来存储编码数据，确保按位存储
bit_array = bitarray()
for bit in encoded:
    bit_array.extend(bit)



print("size of input data: ", asizeof.asizeof(data)/1024/1024)
print("size of encoded data: ", asizeof.asizeof(bit_array)/1024/1024)
print("Decoded data matches original:", decoded_data == data)