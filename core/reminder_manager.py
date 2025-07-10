"""
@文件: reminder_manager.py
@描述: 基于底层数据结构实现的线程安全提醒管理系统
@核心数据结构:
    1. 二级嵌套的defaultdict(list)实现分类存储
    2. 线程安全的回调函数列表
    3. 基于锁的原子操作保护
"""
import threading
from collections import defaultdict
from typing import List, Dict, Callable, Any
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

class ReminderManager:
    def __init__(self):
        """
        初始化数据结构:
        - reminders: 二级嵌套字典，外层为defaultdict(list)，内层为普通list
        - lock: 可重入锁保护数据结构完整性
        - callbacks: 线程安全回调列表
        """
        # 等效于 defaultdict(list) 的纯手工实现
        self._reminders = {}  # type: Dict[str, List[object]]
        self._default_factory = list
        self._lock = threading.RLock()  # 可重入锁
        self._callbacks = []  # type: List[Callable[[dict], None]]
        self._callback_lock = threading.Lock()

    def _get_reminder_list(self, flower_type: str) -> List[object]:
        """线程安全的字典访问方法"""
        with self._lock:
            if flower_type not in self._reminders:
                self._reminders[flower_type] = self._default_factory()
            return self._reminders[flower_type]

    def add_reminder(self, flower_type: str, reminder_system: object) -> None:
        """
        添加提醒系统的底层逻辑:
        1. 获取flower_type对应的提醒列表
        2. 清空现有提醒（如果存在）
        3. 添加新提醒并启动
        """
        with self._lock:
            reminders = self._get_reminder_list(flower_type)
            
            # 清空现有提醒（原子操作）
            while reminders:
                old = reminders.pop()
                old.stop()
            
            # 添加新提醒
            reminders.append(reminder_system)
            reminder_system.start()
            
            # 调试用打印，实际项目应使用logging
            print(f"[ReminderManager] 已为 {flower_type} 添加提醒系统")

    def remove_reminder(self, flower_type: str) -> None:
        """完全移除某类花的提醒"""
        with self._lock:
            if flower_type in self._reminders:
                reminders = self._reminders[flower_type]
                # 原子性停止所有提醒
                for sys in reminders:
                    sys.stop()
                del self._reminders[flower_type]
                print(f"[ReminderManager] 已移除 {flower_type} 的所有提醒")

    def register_callback(self, callback: Callable[[dict], None]) -> None:
        """线程安全的回调注册"""
        with self._callback_lock:
            if callback not in self._callbacks:
                self._callbacks.append(callback)

    def notify(self, event_data: dict) -> None:
        """
        事件通知的完整处理流程:
        1. 打包事件数据
        2. 切换到主线程执行回调
        """
        if not QApplication.instance():
            print("[ERROR] QApplication未初始化")
            return

        # 获取回调的快照（避免长时间持有锁）
        with self._callback_lock:
            callbacks = self._callbacks.copy()

        # 通过Qt信号槽切换到主线程
        def _execute_callbacks():
            for cb in callbacks:
                try:
                    cb(event_data)
                except Exception as e:
                    print(f"[Callback Error] {str(e)}")

        QTimer.singleShot(0, _execute_callbacks)

    def _atomic_dict_operation(self, key: str, operation: Callable[[List], None]) -> None:
        """字典原子操作模板方法"""
        with self._lock:
            container = self._get_reminder_list(key)
            operation(container)

    def __contains__(self, flower_type: str) -> bool:
        """支持 in 操作符"""
        with self._lock:
            return flower_type in self._reminders

    def __len__(self) -> int:
        """获取管理的花种类数"""
        with self._lock:
            return len(self._reminders)

    def cleanup(self) -> None:
        """清理所有资源"""
        with self._lock:
            for flower_type in list(self._reminders.keys()):
                self.remove_reminder(flower_type)
            self._reminders.clear()