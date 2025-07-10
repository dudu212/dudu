from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QFrame
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QPixmap, QFont, QColor, QMouseEvent, QScreen

class ReminderPopup(QDialog):
    def __init__(self, message, flower_type="鲜花", parent=None):
        super().__init__(parent)
        self.setWindowTitle("鲜花养护提醒")
        self.setFixedSize(480, 320)  # 增加宽度以容纳更长的按钮
        
        # 设置无边框和半透明背景
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |  # 保持窗口在最顶层
            Qt.WindowType.FramelessWindowHint |   # 无边框窗口
            Qt.WindowType.Tool |                  # 工具窗口样式
            Qt.WindowType.X11BypassWindowManagerHint  # 在某些系统上绕过窗口管理器
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)  # 无需焦点也能显示
        
        # 创建主框架
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(0, 0, 480, 320)  # 增加宽度
        self.main_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                border: 3px solid #3498db;
            }}
        """)
        
        # 标题标签
        title_label = QLabel(f"{flower_type}养护提醒", self.main_frame)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setGeometry(40, 20, 400, 50)  # 调整位置
        title_label.setStyleSheet("""
            QLabel {
                background-color: #3498db;
                color: white;
                font: bold 18pt '等线';
                border-radius: 10px;
                padding: 5px;
            }
        """)
        
        # 鲜花图标
        icon_label = QLabel(self.main_frame)
        icon_label.setPixmap(QPixmap("backgrounds/bg1.jpg").scaled(100, 100))
        icon_label.setGeometry(190, 80, 100, 100)  # 居中位置
        icon_label.setStyleSheet("""
            QLabel {
                border-radius: 50px;
                border: 2px solid #2c3e50;
            }
        """)
        
        # 消息标签
        message_label = QLabel(message, self.main_frame)
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_label.setGeometry(65, 190, 350, 70)  # 调整位置
        message_label.setStyleSheet("""
            QLabel {
                background-color: rgba(236, 240, 241, 0.8);
                color: #2c3e50;
                font: 14pt '等线';
                border-radius: 10px;
                padding: 10px;
            }
        """)
        message_label.setWordWrap(True)
        
        # 按钮容器（增加宽度）
        button_frame = QFrame(self.main_frame)
        button_frame.setGeometry(115, 270, 250, 40)  # 增加宽度
        button_frame.setStyleSheet("background: transparent;")
        
        # 按钮布局
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(15)  # 增加按钮间距
        
        # 确认按钮（保持原样）
        ok_button = QPushButton("知道了")
        ok_button.setFixedSize(90, 40)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font: bold 12pt '等线';
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        ok_button.clicked.connect(self.accept)
        
        # 稍后提醒按钮（增加宽度以完整显示文字）
        later_button = QPushButton("10分钟后提醒")
        later_button.setFixedSize(120, 40)  # 增加宽度
        later_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font: bold 12pt '等线';
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
        later_button.clicked.connect(self.snooze)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(later_button)
        
        # 自动关闭计时器
        self.close_timer = QTimer(self)
        self.close_timer.setInterval(30000)  # 30秒后自动关闭
        self.close_timer.timeout.connect(self.accept)
        self.close_timer.start()
        
        # 设置窗口位置（右下角）
        self.move_to_corner()
        
        # 拖动支持
        self.drag_position = None
    
    def move_to_corner(self):
        """移动窗口到右下角"""
        screen = QApplication.primaryScreen().geometry()
        self.move(
            screen.width() - self.width() - 20,
            screen.height() - self.height() - 20
        )
    
    def snooze(self):
        """稍后提醒功能"""
        self.close_timer.stop()
        self.rejected.emit()  # 发送取消信号
        self.close()
    
    def mousePressEvent(self, event: QMouseEvent):
        """允许拖动窗口"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """拖动窗口"""
        if self.drag_position and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """释放鼠标"""
        if event.button() == Qt.MouseButton.LeftButton and self.drag_position:
            self.drag_position = None
            event.accept()
    
    def showEvent(self, event):
        """显示窗口时确保在最前面"""
        super().showEvent(event)
        self.activateWindow()
        self.raise_()
        self.setFocus()
        self.move_to_corner()  # 确保每次显示都在右下角
    
    def flash_window(self):
        """闪烁窗口以引起注意"""
        self.flash_count = 5
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self._flash_step)
        self.flash_timer.start(500)  # 500ms间隔


    def showEvent(self, event):
        """窗口显示时的额外处理"""
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
        # 闪烁窗口引起注意
        self.flash_window()

    
    def _flash_step(self):
        """闪烁步骤"""
        if self.flash_count <= 0:
            self.flash_timer.stop()
            self.setStyleSheet("")  # 恢复默认样式
            return
            
        if self.flash_count % 2 == 1:
            # 设置为高亮边框
            self.setStyleSheet("""
                QFrame {
                    border: 3px solid #ff0000;
                    border-radius: 20px;
                }
            """)
        else:
            # 恢复默认边框
            self.setStyleSheet("""
                QFrame {
                    border: 3px solid #3498db;
                    border-radius: 20px;
                }
            """)
        
        self.flash_count -= 1

    