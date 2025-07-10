import time
import threading
from datetime import datetime, timedelta
from .data_structures import ThreadSafeHeap

class FlowerCareReminderSystem:
    """鲜花养护提醒系统核心"""
    def __init__(self, manager, flower_type):
        # 关联的提醒管理器
        self.manager = manager
        # 鲜花类型
        self.flower_type = flower_type
        
        # 使用自定义的线程安全最小堆
        self.event_heap = ThreadSafeHeap()
        # 线程控制标志
        self.running = False
        # 处理线程
        self.thread = None
        
    def add_flower_reminder(self, start_time, interval_days, repeat_count=10):
        """
        添加鲜花养护提醒
        :param start_time: 首次触发时间 (datetime)
        :param interval_days: 提醒间隔天数
        :param repeat_count: 重复次数
        """
        print(f"[提醒系统] 添加提醒: {self.flower_type}, 开始时间: {start_time}, 间隔: {interval_days}天")
        
        # 生成提醒事件序列
        for i in range(repeat_count):
            event_time = start_time + timedelta(days=i * interval_days)
            trigger_timestamp = event_time.timestamp()
            
            # 使用元组存储事件 (触发时间, 事件数据)
            event = (trigger_timestamp, {
                "type": "care_reminder",
                "flower": self.flower_type,
                "trigger_time": event_time,
                "interval_days": interval_days,
                "message": f"【养护提醒】请养护 {self.flower_type} - 下次养护时间: {event_time.strftime('%Y-%m-%d %H:%M')}"
            })
            
            # 线程安全地添加事件
            self.event_heap.push(event)
            print(f"[提醒系统] 添加事件: {event_time.strftime('%Y-%m-%d %H:%M')} - {self.flower_type}")
    
    def start(self):
        """启动提醒系统"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._process_events)
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        """停止提醒系统"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        print(f"[提醒系统] {self.flower_type} 的提醒已停止")
    
    def _process_events(self):
        """后台线程处理提醒事件"""
        print(f"[提醒系统] {self.flower_type} 的后台线程已启动...")
        while self.running:
            try:
                now = time.time()
                events_to_trigger = []
                
                # 获取所有到期的事件
                while not self.event_heap.is_empty():
                    next_event = self.event_heap.peek()
                    if next_event and next_event[0] <= now:
                        event = self.event_heap.pop()
                        events_to_trigger.append(event)
                        print(f"[提醒系统] 弹出到期事件: {event[1]['message']}")
                    else:
                        break
                
                # 触发所有到期的事件
                for event in events_to_trigger:
                    _, event_data = event
                    print(f"[提醒系统] 触发事件: {event_data['message']}")
                    # 通知提醒管理器
                    self.manager.notify(event_data)
                
                # 智能休眠
                sleep_time = 0.5
                if not self.event_heap.is_empty():
                    next_trigger = self.event_heap.peek()[0]
                    sleep_time = min(1.0, max(0.1, next_trigger - now))
                
                time.sleep(sleep_time)
            
            except Exception as e:
                print(f"提醒系统异常: {e}")
                time.sleep(1)
        print(f"[提醒系统] {self.flower_type} 的后台线程已停止")