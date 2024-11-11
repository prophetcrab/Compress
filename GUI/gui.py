import os.path
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QListWidget, QComboBox, QFrame, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from pathlib import Path

from ConnectBlock.HuffmanBlock import *

class CompressionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Compression/Decompression Tool")
        self.setGeometry(100, 100, 600, 500)

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        file_frame = QFrame()
        file_frame_layout = QVBoxLayout()

        self.file_list = QListWidget()
        self.file_list.setAcceptDrops(True)
        self.file_list.setDragEnabled(True)
        self.file_list.setToolTip("Drag and drop files or folders here, or click 'Browse' to select")
        self.setAcceptDrops(True)

        buttons_layout = QHBoxLayout()

        # 浏览文件按钮
        self.file_browse = QPushButton("Browse Files")
        self.file_browse.clicked.connect(self.add_browsed_files)
        buttons_layout.addWidget(self.file_browse)

        # 浏览文件夹按钮
        self.folder_browse = QPushButton("Browse Folders")
        self.folder_browse.clicked.connect(self.add_browsed_folders)
        buttons_layout.addWidget(self.folder_browse)

        self.delete_file_button = QPushButton("Delete Selected")
        self.delete_file_button.clicked.connect(self.delete_selected_file)
        buttons_layout.addWidget(self.delete_file_button)

        file_frame_layout.addWidget(self.file_list)
        file_frame_layout.addLayout(buttons_layout)
        file_frame.setLayout(file_frame_layout)
        left_layout.addWidget(file_frame)
        top_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()

        encoding_layout = QHBoxLayout()
        encoding_label = QLabel("Encoding:")
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["Huffman","LZMA","Arithmetic"])
        encoding_layout.addWidget(encoding_label)
        encoding_layout.addWidget(self.encoding_combo)
        right_layout.addLayout(encoding_layout)

        output_layout = QHBoxLayout()
        output_label = QLabel("Output Directory:")
        self.output_path = QLineEdit()
        self.output_browse = QPushButton("Browse")
        self.output_browse.clicked.connect(self.browse_output)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_path)
        output_layout.addWidget(self.output_browse)
        right_layout.addLayout(output_layout)

        button_layout = QHBoxLayout()
        self.compress_button = QPushButton("Compress")
        self.compress_button.clicked.connect(self.compress)
        self.decompress_button = QPushButton("Decompress")
        self.decompress_button.clicked.connect(self.decompress)
        button_layout.addWidget(self.compress_button)
        button_layout.addWidget(self.decompress_button)
        right_layout.addLayout(button_layout)

        top_layout.addLayout(right_layout)
        main_layout.addLayout(top_layout)

        self.output_log = QTextEdit()
        self.output_log.setReadOnly(True)
        self.output_log.setPlaceholderText("Calling.......")
        main_layout.addWidget(self.output_log)

        self.setLayout(main_layout)

        """DataArea"""
        self.file_path_list = []
        self.save_path = ""
    # 添加浏览文件
    def add_browsed_files(self):
        files = self.browse_files()
        if files:
            for file in files:
                self.file_list.addItem(file)

    # 添加浏览文件夹
    def add_browsed_folders(self):
        folder = self.browse_folder()
        if folder:
            self.file_list.addItem(folder)

    # 浏览文件对话框，返回文件路径
    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        return files

    # 浏览文件夹对话框，返回文件夹路径
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        return folder

    def delete_selected_file(self):
        selected_items = self.file_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Warning", "No File be Selected")
            return

        if not selected_items:
            return
        for item in selected_items:
            self.file_list.takeItem(self.file_list.row(item))

    def browse_output(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        self.save_path = directory
        if directory:
            self.output_path.setText(directory)


    def compress(self):
        """获取file路径"""
        selected_items = self.file_list.selectedItems()

        if not selected_items:
            QMessageBox.warning(self, "Warning", "No File be Selected")
            return
        file = [item.text() for item in selected_items]
        file = file[0]

        """获取output路径"""
        output_dir = self.output_path.text()
        if not output_dir:
            QMessageBox.warning(self, "Warning", "No Output path")
            return

        method = self.encoding_combo.currentText()
        if not method:
            QMessageBox.warning(self, "Warning", "No Encoding Method")
            return

        if method == 'Huffman':
            msg = call_HuffmanCompressor(file, output_dir)
            self.output_log.append(msg)

        for item in selected_items:
            # 删除选中的行
            row = self.file_list.row(item)
            self.file_list.takeItem(row)



    def decompress(self):
        """选中目标文件"""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No File be Selected")
            return
        """获取file路径"""
        file = [item.text() for item in selected_items]
        file = file[0]

        file_extension = os.path.splitext(file)[1]
        if file_extension != ".myzip":
            QMessageBox.warning(self, "Warning", "Can not be decompressed")

        """获取output路径"""
        output_dir = self.output_path.text()
        if not output_dir:
            QMessageBox.warning(self, "Warning", "No Output path")
            return

        method = self.encoding_combo.currentText()
        if not method:
            QMessageBox.warning(self, "Warning", "No Encoding Method")
            return

        if method == "Huffman":
            msg = call_HuffmanDecompressor(file, output_dir)
            self.output_log.append(msg)

        for item in selected_items:
            # 删除选中的行
            row = self.file_list.row(item)
            self.file_list.takeItem(row)

        # self.output_log.append(output_message)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                self.file_list.addItem(file_path)
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CompressionApp()
    ex.show()
    sys.exit(app.exec_())
