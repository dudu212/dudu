from PyQt6.QtWidgets import QMainWindow, QFrame, QCheckBox, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from ui.user_set_ui import UserSetWindow  # 添加导入
from ui.smart_reminder_ui import SmartReminderWindow  # 添加导入

class ReminderChoiceWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.app.add_window(self)
        self.drag_position = None
        self.setup_ui()

        # 添加测试弹窗按钮
        self.test_button = QPushButton("测试弹窗", self)
        self.test_button.setGeometry(300, 300, 100, 30)
        self.test_button.clicked.connect(self.test_popup)


    def test_popup(self):
        """测试弹窗功能"""
        self.app.test_popup_display()
        
    def setup_ui(self):
        # 窗口设置 - 无边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setWindowTitle("提醒方式选择")
        self.resize(800, 600)

        # 创建中央部件
        central_widget = QFrame()
        central_widget.setObjectName("centralwidget")
        central_widget.setStyleSheet("""
            QFrame#centralwidget {
                background-color: #ecf0f1;
                border-radius: 15px;
            }
        """)
        self.setCentralWidget(central_widget)
        
        # 创建框架
        frame = QFrame(central_widget)
        frame.setGeometry(250, 150, 311, 191)
        frame.setObjectName("frame")
        frame.setStyleSheet("""
            QFrame#frame {
                border-radius: 30px;
                background-color: rgba(255, 255, 255, 0.8);
                background-image: url(backgrounds/bg1.jpg);
                border: 2px solid #e0e0e0;
            }
        """)
        
        # 添加标签和复选框
        title_label = QLabel(frame)
        title_label.setGeometry(85, 20, 141, 31)
        title_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: bold 14pt "等线";
                border-radius:10px;
                color: #2c3e50;
                padding: 5px;
            }
        """)
        title_label.setText("选择提醒方式")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.user_checkbox = QCheckBox(frame)
        self.user_checkbox.setGeometry(85, 70, 141, 31)
        self.user_checkbox.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.85);
                font: 12pt "等线";
                border-radius:8px;
                color: #2c3e50;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.user_checkbox.setText("用户设置")
        
        self.smart_checkbox = QCheckBox(frame)
        self.smart_checkbox.setGeometry(85, 120, 141, 31)
        self.smart_checkbox.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.85);
                font: 12pt "等线";
                border-radius:8px;
                color: #2c3e50;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        self.smart_checkbox.setText("智能提醒")
        
        # 添加确定按钮
        confirm_button = QPushButton(central_widget)
        confirm_button.setGeometry(350, 370, 100, 40)
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font: bold 12pt "等线";
                border-radius: 10px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1d6fa5;
            }
        """)
        confirm_button.setText("确定")
        confirm_button.clicked.connect(self.navigate_to_selected)
        

    
    def navigate_to_selected(self):
        """导航到选定的界面"""
        if self.user_checkbox.isChecked():
            # 确保正确导入 UserSetWindow
            self.user_set_window = UserSetWindow(self.app)
            self.user_set_window.show()
            self.hide()
        elif self.smart_checkbox.isChecked():
            # 确保正确导入 SmartReminderWindow
            self.smart_reminder_window = SmartReminderWindow(self.app)
            self.smart_reminder_window.show()
            self.hide()
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件"""
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_position:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()

