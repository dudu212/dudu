import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from core.reminder_manager import ReminderManager
from core.data_analysis import FlowerDataAnalyzer
from ui.reminder_choice_ui import ReminderChoiceWindow

class FlowerCareApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.windows = []  # 跟踪所有打开的窗口
        
        # 创建提醒管理器和数据分析器
        self.reminder_manager = ReminderManager()
        self.analyzer = FlowerDataAnalyzer()

        # 鲜花种类列表
        self.flower_types = ["玫瑰", "百合", "郁金香", "康乃馨", "向日葵"]
        
        # 注册提醒回调
        self.reminder_manager.register_callback(self.show_reminder_popup)
        
        # 创建主窗口
        self.window = ReminderChoiceWindow(self)

    def add_flower_type(self, flower_name):
        """添加新鲜花种类"""
        if flower_name.strip() and flower_name not in self.flower_types:
            self.flower_types.append(flower_name)
            print(f"添加新鲜花种类: {flower_name}")
            return True
        return False

    def add_window(self, window):
        """添加窗口到跟踪列表"""
        self.windows.append(window)
    
    def update_flower_types(self):
        """更新所有窗口的鲜花种类"""
        for window in self.windows:
            if hasattr(window, 'update_flower_list'):
                window.update_flower_list()
    
    def add_flower_type(self, flower_name):
        """添加新鲜花种类"""
        if flower_name.strip() and flower_name not in self.flower_types:
            self.flower_types.append(flower_name)
            self.update_flower_types()  # 通知所有窗口更新
            return True
        return False
    def run(self):
        """运行应用"""
        self.window.show()
        sys.exit(self.app.exec())
        
    def quit(self):
        """退出应用"""
        # 停止所有提醒
        for flower_type in self.reminder_manager.get_active_reminders():
            self.reminder_manager.remove_reminder(flower_type)
    
    def show_reminder_popup(self, event_data):
        """显示提醒弹窗"""
        # 在主线程中显示弹窗
        def show_popup():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(event_data['message'])
            msg.setWindowTitle("鲜花养护提醒")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        
        # 使用 QTimer.singleShot 确保在主线程中执行
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, show_popup)
if __name__ == "__main__":
    flower_app = FlowerCareApp()
    flower_app.run()