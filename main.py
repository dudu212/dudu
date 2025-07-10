import sys
import threading
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QMainWindow, QFrame, QCheckBox, QLabel, QPushButton
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from core.reminder_manager import ReminderManager
from core.data_analysis import FlowerDataAnalyzer
from ui.reminder_choice_ui import ReminderChoiceWindow
from ui.reminder_ui import ReminderPopup

class FlowerCareApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.reminder_manager = ReminderManager()
        self.analyzer = FlowerDataAnalyzer()
        self.reminder_manager.register_callback(self.show_reminder_popup)
        
        self.flower_types = ["玫瑰", "百合", "郁金香", "康乃馨", "向日葵"]
        self.windows = []
        self.window = ReminderChoiceWindow(self)
        self.add_window(self.window)
        self.active_popups = []  # 跟踪活动的弹窗
        self.snooze_timers = {}  # 跟踪稍后提醒的计时器
        
        # 添加测试按钮
        self.window.test_button = QPushButton("测试弹窗", self.window)
        self.window.test_button.setGeometry(300, 300, 100, 30)
        self.window.test_button.clicked.connect(self.test_popup_display)
    
    def test_popup_display(self):
        """测试弹窗显示功能"""
        test_data = {
            "message": "测试弹窗显示功能",
            "flower": "测试鲜花"
        }
        self.show_reminder_popup(test_data)
    
    def add_window(self, window):
        self.windows.append(window)
    
    def update_flower_types(self):
        for window in self.windows:
            if hasattr(window, 'update_flower_list'):
                window.update_flower_list()
    
    def add_flower_type(self, flower_name):
        if flower_name.strip() and flower_name not in self.flower_types:
            self.flower_types.append(flower_name)
            self.update_flower_types()
            return True
        return False
    
    def run(self):
        self.window.show()
        sys.exit(self.app.exec())
    
    def quit(self):
        # 关闭所有弹窗
        for popup in self.active_popups:
            popup.close()
        self.active_popups.clear()
        
        # 停止所有提醒
        for flower_type in list(self.reminder_manager.reminders.keys()):
            self.reminder_manager.remove_reminder(flower_type)
        
        # 停止所有稍后提醒计时器
        for timer in self.snooze_timers.values():
            timer.cancel()
        self.snooze_timers.clear()
    
    def show_reminder_popup(self, event_data):
        print(f"尝试显示弹窗: {event_data['message']}")
        # 使用QTimer.singleShot确保在主线程中执行
        QTimer.singleShot(0, lambda: self._create_popup(event_data))
    
    def _create_popup(self, event_data):
        print(f"当前线程: {threading.current_thread().name}")
        try:
            app = QApplication.instance()
            if not app:
                print("错误: 没有活动的QApplication实例")
                return
                
            print(f"创建提醒弹窗: {event_data['message']}")
            
            # 提取鲜花类型
            flower_type = event_data.get('flower', '鲜花')
            
            # 创建弹窗
            popup = ReminderPopup(event_data['message'], flower_type)
            
            # 连接取消信号（稍后提醒）
            popup.rejected.connect(lambda: self.handle_snooze(event_data))
            
            # 添加到活动弹窗列表
            self.active_popups.append(popup)
            
            # 显示弹窗
            popup.show()
            popup.activateWindow()
            popup.raise_()
            
            # 闪烁弹窗以引起注意
            popup.flash_window()
            
            print(f"弹窗已显示 - {flower_type}提醒")
        except Exception as e:
            print(f"显示弹窗时出错: {e}")

    def handle_snooze(self, event_data):
        """处理稍后提醒请求"""
        flower_type = event_data.get('flower', '鲜花')
        print(f"稍后提醒: {flower_type}")
        
        # 取消现有的稍后提醒计时器
        if flower_type in self.snooze_timers:
            self.snooze_timers[flower_type].cancel()
        
        # 创建新的稍后提醒
        snooze_time = timedelta(minutes=10)
        snooze_time_sec = snooze_time.total_seconds()
        
        # 创建定时器
        timer = threading.Timer(snooze_time_sec, self.trigger_snooze, [event_data])
        timer.start()
        
        # 存储计时器
        self.snooze_timers[flower_type] = timer
        print(f"已设置10分钟后提醒: {flower_type}")
    
    def trigger_snooze(self, event_data):
        """触发稍后提醒"""
        flower_type = event_data.get('flower', '鲜花')
        print(f"触发稍后提醒: {flower_type}")
        
        # 移除计时器
        if flower_type in self.snooze_timers:
            del self.snooze_timers[flower_type]
        
        # 重新显示弹窗
        self.show_reminder_popup(event_data)
    
    def test_reminder_system(self):
        """测试提醒系统功能"""
        print("测试-开始测试提醒系统")
        
        # 测试过去时间
        past_time = datetime.now() - timedelta(days=1)
        self.test_add_reminder("测试鲜花-过去时间", past_time, 1)
        
        # 测试未来时间
        future_time = datetime.now() + timedelta(days=1)
        self.test_add_reminder("测试鲜花-未来时间", future_time, 2)
    
    def test_add_reminder(self, name, start_time, interval):
        """添加测试提醒"""
        from core.reminder_system import FlowerCareReminderSystem
        test_system = FlowerCareReminderSystem(self.reminder_manager, name)
        test_system.add_flower_reminder(
            start_time=start_time,
            interval_days=interval
        )
        self.reminder_manager.add_reminder(name, test_system)
        print(f"测试-{name}提醒已添加")

if __name__ == "__main__":
    flower_app = FlowerCareApp()
    flower_app.test_reminder_system()
    flower_app.run()