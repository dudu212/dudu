from PyQt6.QtWidgets import QMainWindow, QFrame, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt6.QtCore import Qt

class DataAnalysisWindow(QMainWindow):
    def __init__(self, app, flower_name=''):
        super().__init__()
        self.app = app
        self.app.add_window(self)
        self.analyzer = app.analyzer  # 使用应用的数据分析器
        self.setup_ui(flower_name)
        # 添加拖拽支持
        self.drag_position = None
    
    def setup_ui(self, flower_name):
        # 窗口设置 - 无边框
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setWindowTitle("数据分析")
        self.resize(800, 600)
        
        def mousePressEvent(self, event):
            """鼠标按下事件"""
            if event.button() == Qt.MouseButton.LeftButton:
        # 记录鼠标按下时的位置
                self.drag_position = event.globalPosition().toPoint()
                event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.drag_position:
            # 计算窗口需要移动的偏移量
            delta = event.globalPosition().toPoint() - self.drag_position
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

        def mouseReleaseEvent(self, event):
            """鼠标释放事件"""
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag_position = None
            event.accept()
        
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
        frame.setGeometry(150, 80, 501, 401)
        frame.setObjectName("frame")
        frame.setStyleSheet("""
            QFrame#frame {
                border-radius: 30px;
                background-image: url(backgrounds/bg4.jpg);
                background-repeat: no-repeat;
                background-position: center;
                border: 2px solid #e0e0e0;
            }
        """)
        
        # 标题
        title_label = QLabel(frame)
        title_label.setGeometry(150, 30, 201, 41)
        title_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: bold 16pt "等线";
                border-radius:10px;
                color: #2c3e50;
                padding: 5px;
            }
        """)
        title_label.setText("数据记录与统计分析")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 鲜花种类设置
        flower_label = QLabel(frame)
        flower_label.setGeometry(50, 100, 101, 25)
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
        self.flower_input.setGeometry(160, 100, 171, 25)
        self.flower_input.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        self.flower_input.setText(flower_name or "输入鲜花名称...")
        
        # 影响因素选择
        factor_label = QLabel(frame)
        factor_label.setGeometry(50, 150, 101, 25)
        factor_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: 11pt "等线";
                border-radius:5px;
                padding: 3px;
            }
        """)
        factor_label.setText("影响因素:")
        
        self.factor_combo = QComboBox(frame)
        self.factor_combo.setGeometry(160, 150, 171, 25)
        self.factor_combo.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            padding: 5px;
        """)
        self.factor_combo.addItems(["温度", "湿度", "光照", "土壤PH值"])
        
        # 结果显示区域
        result_label = QLabel(frame)
        result_label.setGeometry(50, 200, 101, 25)
        result_label.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.7);
                font: 11pt "等线";
                border-radius:5px;
                padding: 3px;
            }
        """)
        result_label.setText("分析结果:")
        
        self.result_text = QLabel(frame)
        self.result_text.setGeometry(160, 200, 281, 121)
        self.result_text.setStyleSheet("""
            *{
                background-color: rgba(255, 255, 255, 0.85);
                border: 1px solid #bdc3c7;
                border-radius: 10px;
                padding: 10px;
                font: 11pt "等线";
                color: #2c3e50;
            }
        """)
        self.result_text.setText("等待分析...")
        self.result_text.setWordWrap(True)
        
        # 添加分析按钮
        analyze_button = QPushButton(frame)
        analyze_button.setGeometry(180, 340, 141, 31)
        analyze_button.setStyleSheet("""
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
        analyze_button.setText("开始分析")
        analyze_button.clicked.connect(self.perform_analysis)
    
    def perform_analysis(self):
        """执行数据分析"""
        flower_name = self.flower_input.text().strip()
        factor = self.factor_combo.currentText()
        
        if not flower_name:
            self.result_text.setText("错误: 请填写鲜花名称")
            return
        
        # 执行数据分析
        result = self.analyzer.analyze_flower_data(flower_name, factor)
        
        # 显示结果
        result_text = f"鲜花: {flower_name}\n"
        result_text += f"因素: {factor}\n"
        result_text += f"最优值: {result['optimal']}\n"
        result_text += f"建议间隔: {result['interval']}天"
        
        self.result_text.setText(result_text)


    
    def go_back(self):
        """返回智能提醒窗口"""
        from .smart_reminder_ui import SmartReminderWindow
        self.smart_window = SmartReminderWindow(self.app)
        self.smart_window.show()
        self.hide()