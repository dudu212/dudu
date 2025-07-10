import threading
from collections import defaultdict
from .data_structures import ThreadSafeHeap
from datetime import datetime, timedelta

class ReminderManager:
    """管理所有鲜花提醒，确保同一种鲜花只有一种提醒生效"""
    def __init__(self):
        self.reminders = defaultdict(list)  # 鲜花名称 -> [提醒系统实例]
        self.lock = threading.Lock()
        self.callbacks = []  # 提醒回调函数
        
    def add_reminder(self, flower_type, reminder_system):
        """添加新的提醒系统实例"""
        with self.lock:
            # 移除同种鲜花的旧提醒
            if flower_type in self.reminders:
                for old_reminder in self.reminders[flower_type]:
                    old_reminder.stop()
                self.reminders[flower_type].clear()
            
            # 添加新提醒
            self.reminders[flower_type].append(reminder_system)
            reminder_system.start()
            
            print(f"[提醒管理器] 为 {flower_type} 添加新提醒")
    
    def remove_reminder(self, flower_type):
        """移除指定鲜花的提醒"""
        with self.lock:
            if flower_type in self.reminders:
                for reminder in self.reminders[flower_type]:
                    reminder.stop()
                del self.reminders[flower_type]
                print(f"[提醒管理器] 移除 {flower_type} 的提醒")
    
    def get_active_reminders(self):
        """获取所有活动的提醒"""
        with self.lock:
            return list(self.reminders.keys())
    
    def register_callback(self, callback):
        """注册提醒回调函数"""
        self.callbacks.append(callback)
    
    def notify(self, event_data):
        """通知所有回调函数"""
        for callback in self.callbacks:
            try:
                callback(event_data)
            except Exception as e:
                print(f"提醒回调出错: {e}")