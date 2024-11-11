from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "huffman",
        ["CompressEncoder/Huffman.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
    ),
]

setup(
    name="huffman",
    version="1.0",
    ext_modules=ext_modules,
)
