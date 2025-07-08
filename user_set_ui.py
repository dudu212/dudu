from PyQt6.QtWidgets import QMainWindow, QFrame, QLabel, QLineEdit, QPushButton, QDateTimeEdit, QComboBox
from PyQt6.QtCore import Qt

class UserSetWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("用户设置")
        self.resize(800, 600)
        
        # 创建中央部件
        central_widget = QFrame()
        central_widget.setObjectName("centralwidget")
        central_widget.setStyleSheet("""
            background-color: #ecf0f1;
        """)
        self.setCentralWidget(central_widget)
        
        # 创建返回按钮
        back_button = QPushButton(central_widget)
        back_button.setGeometry(20, 20, 80, 30)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font: bold 10pt "等线";
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        back_button.setText("返回")
        back_button.clicked.connect(self.go_back)
        
        # 创建主框架
        frame = QFrame(central_widget)
        frame.setGeometry(150, 100, 501, 351)
        frame.setObjectName("frame")
        frame.setStyleSheet("""
            *{ 
                border-radius:10px; 
                background-color: rgba(255, 255, 255, 0.9);
            }
            QFrame#frame {
                border-radius: 30px;
                background-image: url(backgrounds/bg2.jpg);
                background-repeat: no-repeat;
                background-position: center;
                border: 2px solid #e0e0e0;
            }
        """)
        
        # 标题
        title_label = QLabel(frame)
        title_label.setGeometry(200, 20, 101, 31)
        title_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: bold 14pt "等线";
                border-radius:10px;
                color: #2c3e50;
                padding: 5px;
            }
        """)
        title_label.setText("用户设置")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 修正这里
        
        # 鲜花种类设置
        flower_label = QLabel(frame)
        flower_label.setGeometry(50, 70, 101, 25)
        flower_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: 11pt "等线";
                border-radius:5px;
                padding: 3px;
            }
        """)
        flower_label.setText("鲜花种类:")
        
        self.flower_input = QLineEdit(frame)
        self.flower_input.setGeometry(160, 70, 171, 25)
        self.flower_input.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        self.flower_input.setPlaceholderText("输入鲜花名称...")
        
        # 时间设置
        time_label = QLabel(frame)
        time_label.setGeometry(50, 120, 101, 25)
        time_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: 11pt "等线";
                border-radius:5px;
                padding: 3px;
            }
        """)
        time_label.setText("起始时间:")
        
        self.time_edit = QDateTimeEdit(frame)
        self.time_edit.setGeometry(160, 120, 171, 25)
        self.time_edit.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        
        # 间隔天数设置
        interval_label = QLabel(frame)
        interval_label.setGeometry(50, 170, 101, 25)
        interval_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: 11pt "等线";
                border-radius:5px;
                padding: 3px;
            }
        """)
        interval_label.setText("间隔天数:")
        
        self.interval_combo = QComboBox(frame)
        self.interval_combo.setGeometry(160, 170, 171, 25)
        self.interval_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        
        # 填充间隔天数选项
        for i in range(1, 31):
            self.interval_combo.addItem(f"{i}天")
            
        # 添加确定按钮
        confirm_button = QPushButton(frame)
        confirm_button.setGeometry(200, 250, 101, 31)
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font: bold 12pt "等线";
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1d6fa5;
            }
        """)
        confirm_button.setText("保存设置")
        
        # 添加数据分析按钮
        data_button = QPushButton(central_widget)
        data_button.setGeometry(650, 500, 120, 40)
        data_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                font: bold 11pt "等线";
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        data_button.setText("数据分析")
    
    def go_back(self):
        from reminder_choice_ui import ReminderChoiceWindow
        self.main_window = ReminderChoiceWindow(self.app)
        self.main_window.show()
        self.hide()