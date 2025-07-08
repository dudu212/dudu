#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@ File        : FlowerSpring.py
@ Author      : yqbao
@ Version     : V1.0.0
@ Description :界面集成7.2,需要从my_logmanger中导入具体内容
"""

import os
import sys
import json
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QScrollArea,QFrame, 
    QTextEdit, QComboBox, QToolBar, QMenu, QMessageBox,QFileDialog,QDialog
)
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QCursor
from mylog_manager import LogManager



class LogWriter(QWidget):
    """日志写入界面"""
    def __init__(self, log_manager, plant_name, parent=None):
        super().__init__(parent)
        self.log_manager = log_manager
        self.plant_name = plant_name
        self.selected_image = None
        
        # 创建UI组件
        self.setup_ui()
    
    def setup_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel(f"记录「{self.plant_name}」的养护日志")
        # title.setFont(QFont("Arial", 16, QFontWeight.Bold))
        title.setStyleSheet("color: #2e7d32;")
        layout.addWidget(title)
        
        # 内容编辑区
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("在这里详细记录您的养护过程...")
        self.editor.setFont(QFont("Arial", 12))
        self.editor.setStyleSheet("""
            QTextEdit {
                background-color: #fffde7; 
                border: 1px solid #fff59d;
                border-radius: 5px;
                padding: 15px;
                min-height: 200px;
            }
        """)
        layout.addWidget(self.editor, 1)  # 设置拉伸因子
        
        # 信息工具栏
        self.setup_toolbar(layout)
        select_image_button = QPushButton("选择照片")
        select_image_button.clicked.connect(self.select_image)
        layout.addWidget(select_image_button)
        # 保存按钮
        save_button = QPushButton("保存日志")
        # save_button.setFont(QFont("Arial", 12, QFont.Bold))
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        save_button.clicked.connect(self.save_log)
        layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignRight)
    
    def setup_toolbar(self, main_layout):
        """设置信息工具栏"""
        toolbar = QHBoxLayout()
        
        # 天气选择
        weather_label = QLabel("天气:")
        self.weather_combo = QComboBox()
        self.weather_combo.addItems(["晴", "多云", "阴", "小雨", "大雨", "雪"])
        self.weather_combo.setCurrentIndex(0)
        
        # 生长阶段
        growth_label = QLabel("生长阶段:")
        self.growth_combo = QComboBox()
        self.growth_combo.addItems(["幼苗期", "生长期", "成熟期", "开花期", "休眠期"])
        self.growth_combo.setCurrentIndex(0)
        
        toolbar.addWidget(weather_label)
        toolbar.addWidget(self.weather_combo)
        toolbar.addWidget(growth_label)
        toolbar.addWidget(self.growth_combo)
        toolbar.addStretch()
        
        # 表情按钮
        emoji_button = QPushButton("😊")
        emoji_button.setFont(QFont("Arial", 16))
        emoji_button.setFixedSize(40, 40)
        emoji_button.setStyleSheet("border-radius: 20px;")
        emoji_button.clicked.connect(self.show_emoji_panel)
        
        toolbar.addWidget(emoji_button)
        main_layout.addLayout(toolbar)
    
    def show_emoji_panel(self):
        """显示表情面板"""
        # 简化的表情选择器（实际中可以扩展为带多个表情的面板）
        emojis = ["😊", "😢", "😡", "😎", "😍", "🤔", "🥰", "🤩", "🥳"]
        
        menu = QMenu(self)
        for emoji in emojis:
            action = QAction(emoji, self)
            action.triggered.connect(lambda _, e=emoji: self.insert_emoji(e))
            menu.addAction(action)
        
        menu.exec(QCursor.pos())
    
    def insert_emoji(self, emoji):
        """在当前位置插入表情符号"""
        self.editor.insertPlainText(emoji)
    def get_image_file_path(self):
        """选择照片并获取图片路径"""
        try:
            file_dialog = QFileDialog()
            file_dialog.setNameFilter("图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)")
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

            if file_dialog.exec():
                file_paths = file_dialog.selectedFiles()
                if file_paths:
                    file_path = file_paths[0]
                    if os.path.exists(file_path):
                        return file_path
                    else:
                        QMessageBox.warning(self, "警告", "选择的文件不存在，请重新选择。")
                else:
                    QMessageBox.warning(self, "警告", "未选择任何文件，请重新选择。")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"选择图片时发生错误: {str(e)}")
        return None
    def select_image(self):
        '''选择照片'''
        file_path  = self.get_image_file_path()
        if file_path:
            self.selected_image = file_path
        # file_dialog = QFileDialog()
        # file_dialog.setNameFilter("图片文件(*.png *.jpg *.jpeg)")
        # if file_dialog.exec():
        #     file_path = file_dialog.selectedFiles()
        #     if file_path:
        #         self.selected_image = file_path[0]
    def save_log(self):
        """保存日志"""
        content = self.editor.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "警告", "日志内容不能为空！")
            return

        # 添加天气信息
        weather = self.weather_combo.currentText()
        growth = self.growth_combo.currentText()
        if not weather or not growth:
            QMessageBox.warning(self, "warning", "weather and groth!")
            return
        # 在日志内容前添加标签
        final_content = f"[{growth}][{weather}] {content}"
        # 创建日志条目
        self.log_manager.add_log(self.plant_name, final_content,weather,growth,self.selected_image)     #调用了log_manager,并给image参数传入了由select_image得到的文件路径
        # # 更新日志内容
        # if self.log_manager.logs.last_added:
        #     self.log_manager.logs.last_added.content = final_content
        
        # 保存到文件
        self.log_manager.save_to_file()
        
        QMessageBox.information(self, "成功", "日志已保存！")
        self.editor.clear()
        self.selected_image = None  # 保存后清空选中的图片路径

#设置页面内容
class MainWindow(QMainWindow):
    """主窗口集成日志功能"""
    def __init__(self):
        super().__init__()
        self.log_manager = LogManager()
        self.log_manager.load_from_file()  # 从文件加载现有日志
        
        self.setWindowTitle("养花日志系统")
        self.setGeometry(100, 100, 800, 600)
        
        self.setup_ui()
    
    def setup_ui(self):
        # 中心部件
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # 植物选择视图
        self.plants_view = self.create_plants_view()
        self.stack.addWidget(self.plants_view)
        
        # 日志编写视图
        self.log_writer = None
        
        # 创建工具栏
        self.create_toolbar()
        #  '''创建顶部工具栏'''
    def create_toolbar(self):
        toolbar = self.addToolBar("操作")
        # 返回按钮
        back_action = QAction(QIcon.fromTheme("go-previous"), "返回", self)
        back_action.triggered.connect(self.show_plants_view)
        toolbar.addAction(back_action)
        
        # 日志查看按钮
        view_logs_action = QAction(QIcon.fromTheme("view-list-details"), "查看上一次日志", self)
        view_logs_action.triggered.connect(self.show_recentlog_view)
        toolbar.addAction(view_logs_action)

        # 日志记录按钮
        view_logs_action = QAction(QIcon.fromTheme("view-list-details"), "查看所有日志", self)
        view_logs_action.triggered.connect(self.show_logs_view)
        toolbar.addAction(view_logs_action)
        
        # 保存所有日志按钮
        save_action = QAction(QIcon.fromTheme("document-save"), "保存所有", self)
        save_action.triggered.connect(lambda: self.log_manager.save_to_file())
        toolbar.addAction(save_action)
    
    def create_plants_view(self):
        """创建植物选择视图"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 标题
        title = QLabel("My Flower Spring")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet("color: #2e7d32;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 植物网格容器
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        plants_layout = QHBoxLayout(scroll_content)
        
        # 添加示例植物（实际应用中应从数据源加载）
        plant_names = ["玫瑰", "百合", "兰花", "多肉"]
        for name in plant_names:
            plant_card = QPushButton(name)
            plant_card.setFont(QFont("Arial", 14))
            plant_card.setFixedSize(150, 150)
            plant_card.setStyleSheet("""
                QPushButton {
                    background-color: #e8f5e9;
                    border: 2px solid #c8e6c9;
                    border-radius: 10px;
                    padding: 20px;
                }
                QPushButton:hover {
                    border: 2px solid #4CAF50;
                    background-color: #dcf0dd;
                }
            """)
            plant_card.clicked.connect(lambda checked, n=name: self.open_log_writer(n))
            plants_layout.addWidget(plant_card)
        
        # 添加植物按钮
        add_plant_btn = QPushButton("＋添加植物")
        add_plant_btn.setFixedSize(150, 150)
        add_plant_btn.setFont(QFont("Arial", 14))
        add_plant_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border: 2px dashed #c8e6c9;
                border-radius: 10px;
                padding: 20px;
                color: #757575;
            }
            QPushButton:hover {
                border: 2px dashed #4CAF50;
                background-color: #f0fff4;
            }
        """)
        plants_layout.addWidget(add_plant_btn)
        
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)
        
        return widget
    
    def open_log_writer(self, plant_name):
        """打开日志编写界面"""
        self.log_writer = LogWriter(self.log_manager, plant_name, self)
        self.stack.addWidget(self.log_writer)
        self.stack.setCurrentWidget(self.log_writer)
    
    def show_recentlog_view(self):
        """显示日志查看界面"""
        # 简化实现，实际应创建完整日志浏览界面
        # last_logs = self.log_manager.get_recent_logs(10)
        last_log = self.log_manager.last_added
        if last_log:
            dialog = QDialog(self)
            dialog.setWindowTitle("日志记录")
            layout = QVBoxLayout(dialog)

            log_info = QLabel(f"{last_log.date.strftime('%m-%d %H:%M')} {last_log.plant_name}: {last_log.content}")
            layout.addWidget(log_info)

            if last_log.image:
                pixmap = QPixmap(last_log.image)
                if not pixmap.isNull():
                     # 获取图片原始尺寸
                    original_width = pixmap.width()
                    original_height = pixmap.height()
                    # 限制最大缩放尺寸
                    max_width = 640
                    max_height = 640
                    # 计算缩放比例
                    scale_width = max_width / original_width
                    scale_height = max_height / original_height
                    scale_factor = min(scale_width, scale_height, 1.0)  # 确保不超过原始尺寸
                    new_width = int(original_width * scale_factor)
                    new_height = int(original_height * scale_factor)
                    # 使用高质量抗锯齿缩放算法
                    pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    image_label = QLabel()
                    image_label.setPixmap(pixmap)
                    layout.addWidget(image_label)
                    # pixmap = pixmap.scaled(640, 640, Qt.AspectRatioMode.KeepAspectRatio)
                    # image_label = QLabel()
                    # image_label.setPixmap(pixmap)
                    # layout.addWidget(image_label)

            dialog.exec()
        else:
            QMessageBox.information(self, "日志记录", "还没有输入日志。")

        # msg = "你写入的日志:\n"
        # for log in last_logs:
        #     msg += f"\n{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content[:]}"
            # dialog.exec()
            # if log:
            #     dialog = QDialog(self)
            #     dialog.setWindowTitle("日志记录")
            #     layout = QVBoxLayout(dialog)

            #     log_info = QLabel(f"{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content}")
            #     layout.addWidget(log_info)
            # if log.image:
            #     dialog = QDialog(self)
            #     pixmap = QPixmap(log.image)
            #     if not pixmap.isNull():
            #         # 获取图片原始尺寸
            #         original_width = pixmap.width()
            #         original_height = pixmap.height()
            #         # 限制最大缩放尺寸
            #         max_width = 640
            #         max_height = 640
            #         # 计算缩放比例
            #         scale_width = max_width / original_width
            #         scale_height = max_height / original_height
            #         scale_factor = min(scale_width, scale_height, 1.0)  # 确保不超过原始尺寸
            #         new_width = int(original_width * scale_factor)
            #         new_height = int(original_height * scale_factor)
            #         # 使用高质量抗锯齿缩放算法
            #         pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            #         image_label = QLabel()
            #         image_label.setPixmap(pixmap)
            #         layout.addWidget(image_label)
                        # pixmap = pixmap.scaled(640, 640, Qt.AspectRatioMode.KeepAspectRatio)
                        # image_label = QLabel()
                        # image_label.setPixmap(pixmap)
                        # layout.addWidget(image_label)

            # dialog.exec()
        # QMessageBox.information(self, "日志记录", msg)
    # def show_logs_view(self):
    #     """显示日志列表视图"""
    #     last_logs = self.log_manager.get_recent_logs(10)
    #     msg = "你写入的日志:\n"
    #     for log in last_logs:
    #         if log.image:
    #             dialog  = QDialog(self)
    #             layout = QVBoxLayout(dialog)
    #             log_info = QLabel(f"{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content}")
    #             layout.addWidget(log_info)
    #             pixmap = QPixmap(log.image)
    #             if not pixmap.isNull():
    #                  # 获取图片原始尺寸
    #                 original_width = pixmap.width()
    #                 original_height = pixmap.height()
    #                 # 限制最大缩放尺寸
    #                 max_width = 640
    #                 max_height = 640
    #                 # 计算缩放比例
    #                 scale_width = max_width / original_width
    #                 scale_height = max_height / original_height
    #                 scale_factor = min(scale_width, scale_height, 1.0)  # 确保不超过原始尺寸
    #                 new_width = int(original_width * scale_factor)
    #                 new_height = int(original_height * scale_factor)
    #                 # 使用高质量抗锯齿缩放算法
    #                 pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    #                 image_label = QLabel()
    #                 image_label.setPixmap(pixmap)
    #                 layout.addWidget(image_label)
    #                 # pixmap = pixmap.scaled(640, 640, Qt.AspectRatioMode.KeepAspectRatio)
    #                 # image_label = QLabel()
    #                 # image_label.setPixmap(pixmap)
    #                 # layout.addWidget(image_label)
    #                 dialog.exec()
    #         msg += f"\n{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content[:]}"
    #     QMessageBox.information(self, "日志记录", msg)
    def show_logs_view(self):
    # """显示日志列表视图"""
        last_logs = self.log_manager.get_recent_logs()
    
        # 创建主窗口和布局
        dialog = QDialog(self)
        dialog.setWindowTitle("日志记录")
        dialog.resize(800, 600)
    
        # 创建可滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
    
        # 创建内容部件
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # 顶部对齐
    
        # 添加所有日志
        if not last_logs:
            layout.addWidget(QLabel("暂无日志记录"))
        else:
            for log in last_logs:
                # 创建日志条目容器
                log_frame = QFrame()
                log_frame.setFrameShape(QFrame.Shape.Box)
                log_layout = QVBoxLayout(log_frame)
                
                # 添加日志基本信息
                log_info = QLabel(f"{log.date.strftime('%m-%d %H:%M')} {log.plant_name}: {log.content}")
                log_layout.addWidget(log_info)
                
                # 添加图片（如果有）
                if log.image:
                    pixmap = QPixmap(log.image)
                    if not pixmap.isNull():
                        # 缩放图片（保持宽高比）
                        scaled = pixmap.scaled(
                            640, 
                            480, 
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        image_label = QLabel()
                        image_label.setPixmap(scaled)
                        log_layout.addWidget(image_label)
                
                # 添加间距分隔符
                log_layout.addSpacing(20)
                layout.addWidget(log_frame)
        
        # 设置滚动区域内容
        scroll_area.setWidget(content_widget)
        
        # 设置对话框主布局
        main_layout = QVBoxLayout(dialog)
        main_layout.addWidget(scroll_area)
        
        # 添加确定按钮
        btn_ok = QPushButton("确定")
        btn_ok.clicked.connect(dialog.accept)
        main_layout.addWidget(btn_ok)
        
        dialog.exec()
    
    def show_plants_view(self):
        """显示植物列表视图"""
        self.stack.setCurrentWidget(self.plants_view)
        

class FlowerSpring(QApplication):
    """养花日志应用"""
    def __init__(self, argv):
        super().__init__(argv)
        self.window = MainWindow()
        self.window.resize(800,600)
        self.window.show()


if __name__ == "__main__":
    app = FlowerSpring(sys.argv)
    sys.exit(app.exec())
