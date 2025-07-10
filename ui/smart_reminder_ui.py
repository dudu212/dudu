from PyQt6.QtWidgets import QMainWindow, QFrame, QLabel, QPushButton, QDateTimeEdit, QComboBox
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QIcon, QMouseEvent
from core.data_analysis import FlowerDataAnalyzer
from core.reminder_system import FlowerCareReminderSystem

class SmartReminderWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.app.add_window(self)
        self.analyzer = FlowerDataAnalyzer()  # 创建数据分析器
        self.setup_ui()
        self.drag_start_position = None
        self.drag_window_position = None
        
    def setup_ui(self):
        # 窗口设置 - 无边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setWindowTitle("智能提醒")
        self.resize(800, 600)
        
        # 创建中央部件
        central_widget = QFrame()
        central_widget.setObjectName("centralwidget")
        central_widget.setStyleSheet("""
            QFrame#centralwidget {
                background-color: #ecf0f1;
                border-radius: 15px;
                border: 1px solid #bdc3c7;
            }
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
            QFrame#frame {
                border-radius: 30px;
                background-image: url(backgrounds/bg3.jpg);
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
        title_label.setText("智能提醒")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 鲜花种类设置 - 使用选择框
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
        
        # 使用下拉选择框选择鲜花种类
        self.flower_combo = QComboBox(frame)
        self.flower_combo.setGeometry(160, 70, 171, 25)
        self.flower_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        
        # 从主应用获取鲜花种类列表
        self.flower_combo.addItems(self.app.flower_types)

        # 添加新种类按钮
        self.add_flower_button = QPushButton(frame)
        self.add_flower_button.setGeometry(340, 70, 31, 25)
        self.add_flower_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font: bold 10pt "等线";
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.add_flower_button.setText("+")
        self.add_flower_button.clicked.connect(self.show_add_flower_dialog)

        # 添加新种类输入框
        self.new_flower_input = QLineEdit(frame)
        self.new_flower_input.setGeometry(160, 100, 171, 25)
        self.new_flower_input.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        self.new_flower_input.setPlaceholderText("输入新鲜花种类...")
        self.new_flower_input.hide()
        
        # 时间设置
        time_label = QLabel(frame)
        time_label.setGeometry(50, 140, 101, 25)  # 调整位置
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
        self.time_edit.setGeometry(160, 140, 171, 25)  # 调整位置
        self.time_edit.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        self.time_edit.setDateTime(QDateTime.currentDateTime())
        
        # 推荐间隔天数
        interval_label = QLabel(frame)
        interval_label.setGeometry(50, 180, 101, 25)  # 调整位置
        interval_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: 11pt "极线";
                border-radius:5px;
                padding: 3px;
            }
        """)
        interval_label.setText("推荐间隔:")
        
        self.interval_combo = QComboBox(frame)
        self.interval_combo.setGeometry(160, 180, 171, 25)  # 调整位置
        self.interval_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5极;
            padding: 5px;
        """)
        self.interval_combo.setEnabled(False)  # 用户不能直接编辑
        
        # 添加分析按钮
        self.analyze_button = QPushButton(frame)
        self.analyze_button.setGeometry(160, 230, 101, 31)  # 调整位置
        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font: bold 12pt "等线";
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.analyze_button.setText("分析数据")
        self.analyze_button.clicked.connect(self.analyze_flower)
        
        # 添加保存按钮
        self.save_button = QPushButton(frame)
        self.save_button.setGeometry(280, 230, 101, 31)  # 调整位置
        self.save_button.setStyleSheet("""
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
        """)
        self.save_button.setText("保存设置")
        self.save_button.clicked.connect(self.save_settings)
        
        # 状态标签
        self.status_label = QLabel(central_widget)
        self.status_label.setGeometry(150, 470, 500, 40)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            *{
                font: 12pt "等线";
                color: #27ae60;
                border-radius: 5px;
                background-color: rgba(255, 255, 255, 0.7);
                padding: 5px;
            }
        """)
        self.status_label.hide()
    
    def update_flower_list(self):
        """更新鲜花种类下拉框"""
        current_text = self.flower_combo.currentText()
        self.flower_combo.clear()
        self.flower_combo.addItems(self.app.flower_types)
        self.flower_combo.setCurrentText(current_text)


    def show_add_flower_dialog(self):
        """显示添加新鲜花种类的输入框"""
        if self.new_flower_input.isHidden():
            self.new_flower_input.show()
            self.add_flower_button.setText("✓")
        else:
            # 添加新种类
            new_flower = self.new_flower_input.text().strip()
            if new_flower:
                if self.app.add_flower_type(new_flower):
                    # 添加到当前下拉框
                    self.flower_combo.addItem(new_flower)
                    self.flower_combo.setCurrentText(new_flower)
                    
                    # 通知主应用更新鲜花种类列表
                    self.app.update_flower_types()
                    
                    self.show_status(f"成功添加 {new_flower} 种类")
                else:
                    self.show_status("鲜花种类已存在或无效", is_error=True)
            self.new_flower_input.hide()
            self.new_flower_input.clear()
            self.add_flower_button.setText("+")

    def analyze_flower(self):
        """分析鲜花数据并获取推荐间隔"""
        flower_name = self.flower_combo.currentText().strip()
        if not flower_name:
            self.show_status("错误：请选择鲜花种类！", is_error=True)
            return
        
        # 获取推荐间隔天数
        interval = self.analyzer.get_recommended_interval(flower_name)
        
        # 清空并添加推荐结果
        self.interval_combo.clear()
        self.interval_combo.addItem(f"{interval}天")
        
        # 显示成功信息
        self.show_status(f"成功为 {flower_name} 分析推荐间隔！")
        
        # 添加数据点到分析器（模拟用户记录）
        self.analyzer.add_data_point(flower_name, int(interval))
    
    def save_settings(self):
        """保存智能提醒设置"""
        flower_name = self.flower_combo.currentText().strip()
        if not flower_name:
            self.show_status("错误：请选择鲜花种类！", is_error=True)
            return
        
        # 获取用户设置的开始时间和推荐间隔
        start_time = self.time_edit.dateTime().toPyDateTime()
        interval_days = float(self.interval_combo.currentText().rstrip('天'))
        
        # 创建新的提醒系统
        reminder_system = FlowerCareReminderSystem(self.app.reminder_manager, flower_name)
        reminder_system.add_flower_reminder(
            start_time=start_time,
            interval_days=interval_days
        )
        
        # 添加到提醒管理器（这会覆盖旧提醒）
        self.app.reminder_manager.add_reminder(flower_name, reminder极ystem)
        
        # 显示成功信息
        self.show_status(f"成功为 {flower_name} 设置智能提醒！")
        
    def show_status(self, message, is_error=False):
        """显示操作状态信息"""
        self.status_label.show()
        if is_error:
            self.status_label.setStyleSheet("""
                *{
                    font: 12pt "等线";
                    color: #e74c3c;
                    border-radius: 5px;
                    background-color: rgba(255, 255, 255, 0.7);
                    padding: 5px;
                }
            """)
        else:
            self.status_label.setStyleSheet("""
                *{
                    font: 12pt "等线";
                    color: #27ae60;
                    border-radius: 5px;
                    background-color: rgba(255, 255, 255, 0.7);
                    padding: 5px;
                }
            """)
        
        self.status_label.setText(message)
        
        # 3秒后隐藏
        import threading
        timer = threading.Timer(3.0, lambda: self.status_label.hide())
        timer.start()
    
    def go_back(self):
        """返回主窗口"""
        from .reminder_choice_ui import ReminderChoiceWindow
        self.main_window = ReminderChoiceWindow(self.app)
        self.main_window.show()
        self.hide()
        
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint()
            self.drag_window_position = self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_start_position:
            delta = event.globalPosition().toPoint() - self.drag_start_position
            self.move(self.drag_window_position + delta)
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = None
            self.drag_window_position = None
            event.accept()