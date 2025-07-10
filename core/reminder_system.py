import time
import threading
from datetime import datetime, timedelta
from core.data_structures import ThreadSafeMinHeap as ThreadSafeHeap
from PyQt6.QtCore import Qt, QTimer

class FlowerCareReminderSystem:
    def __init__(self, manager, flower_type):
        self.event_heap = ThreadSafeHeap()
        self.running = False
        self.thread = None
        self.manager = manager
        self.flower_type = flower_type
        self.last_processed = 0
        self.lock = threading.Lock()
    
    def add_flower_reminder(self, start_time, interval_days, repeat_count=10):
        print(f"提醒系统-添加提醒: {self.flower_type}, 开始时间: {start_time}, 间隔: {interval_days}天")
        
        current_time = datetime.now()
        
        # 确保使用用户设置的时间部分
        set_time = start_time.time()
        
        # 今天的提醒时间（使用用户设置的时间）
        today_remind_time = datetime.combine(current_time.date(), set_time)
        
        # 1. 如果今天的提醒时间已过，调整到明天
        # 2. 但确保即使是今天的提醒时间已过，也立即添加一个今天的提醒
        immediate_remind_time = None
        
        if today_remind_time <= current_time:
            tomorrow_remind_time = today_remind_time + timedelta(days=1)
            print(f"警告: 设置时间已过，但仍将今天提醒，添加今天+明天双重提醒")
            
            # 添加今天立即提醒（1分钟后触发）
            immediate_remind_time = current_time + timedelta(minutes=1)
            immediate_event = (immediate_remind_time.timestamp(), {
                "type": "immediate_reminder",
                "flower": self.flower_type,
                "trigger_time": immediate_remind_time,
                "interval_days": interval_days,
                "message": f"[设置确认] {self.flower_type}提醒设置成功！今日将再次提醒: {tomorrow_remind_time.strftime('%H:%M')}"
            })
            
            # 添加明天正常提醒
            tomorrow_event = (tomorrow_remind_time.timestamp(), {
                "type": "care_reminder",
                "flower": self.flower_type,
                "trigger_time": tomorrow_remind_time,
                "interval_days": interval_days,
                "message": f"[养护提醒] 请养护{self.flower_type} - 提醒时间: {tomorrow_remind_time.strftime('%Y-%m-%d %H:%M:%S')}"
            })
            
            with self.lock:
                self.event_heap.push(immediate_event)
                self.event_heap.push(tomorrow_event)
            
            print(f"提醒系统-添加今日提醒: {immediate_remind_time.strftime('%H:%M')}")
            print(f"提醒系统-添加明日提醒: {tomorrow_remind_time.strftime('%Y-%m-%d %H:%M')}")
            
            # 今天提醒作为基准时间
            today_remind_time = tomorrow_remind_time
        else:
            # 今天的提醒时间还未到，只添加今天提醒
            today_event = (today_remind_time.timestamp(), {
                "type": "care_reminder",
                "flower": self.flower_type,
                "trigger_time": today_remind_time,
                "interval_days": interval_days,
                "message": f"[养护提醒] 请养护{self.flower_type} - 提醒时间: {today_remind_time.strftime('%Y-%m-%d %H:%M:%S')}"
            })
            with self.lock:
                self.event_heap.push(today_event)
            print(f"提醒系统-添加今日提醒: {today_remind_time.strftime('%H:%M')}")
        
        # 添加后续按间隔的提醒事件（从明天开始）
        for i in range(1, repeat_count):
            next_time = today_remind_time + timedelta(days=i * interval_days)
            
            # 创建后续提醒事件
            next_event = (next_time.timestamp(), {
                "type": "care_reminder",
                "flower": self.flower_type,
                "trigger_time": next_time,
                "interval_days": interval_days,
                "message": f"[养护提醒] 请养护{self.flower_type} - 下次养护时间: {next_time.strftime('%Y-%m-%d %H:%M:%S')}"
            })
            with self.lock:
                self.event_heap.push(next_event)
            print(f"提醒系统-添加事件: {next_time.strftime('%m-%d %H:%M')}")
    
    def start(self):
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._process_events)
        self.thread.daemon = True
        self.thread.start()
        print(f"提醒系统-{self.flower_type}的后台线程启动中...")
    
    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        print(f"提醒系统-{self.flower_type}的后台线程已停止")
    
    def _process_events(self):
        print(f"提醒系统-{self.flower_type}的后台线程开始处理事件")
        while self.running:
            try:
                now = time.time()
                
                # 处理待触发事件
                self._process_pending_events(now)
                
                # 计算下次检查时间
                sleep_time = self._calculate_sleep_time(now)
                if sleep_time > 0:
                    print(f"提醒系统-休眠 {sleep_time:.1f} 秒")
                time.sleep(max(0.1, sleep_time))
            except Exception as e:
                print(f"提醒系统处理异常: {e}")
                time.sleep(1)
        print(f"提醒系统-{self.flower_type}的后台线程结束")
    
    def _process_pending_events(self, now):
        # 使用线程锁确保线程安全
        with self.lock:
            events_to_trigger = []
            
            # 处理所有到期事件
            while not self.event_heap.is_empty():
                next_event = self.event_heap.peek()
                if not next_event:
                    break
                
                event_time = datetime.fromtimestamp(next_event[0])
                current_time = datetime.fromtimestamp(now)
                time_diff = next_event[0] - now
                
                # 打印待检查事件的详细信息
                print(f"检查事件: 类型={next_event[1]['type']}, 事件时间={event_time}, 当前时间={current_time}, 时间差={time_diff:.1f}秒")
                
                # 如果事件时间 <= 当前时间，则触发
                if next_event[0] <= now:
                    event = self.event_heap.pop()
                    if event:
                        _, event_data = event
                        events_to_trigger.append(event_data)
                        print(f"提醒系统-弹出到期事件: {event_data['message']}")
                else:
                    break  # 事件在将来，停止检查
            
            # 释放锁后处理通知
            # 因为通知可能会执行较长时间的操作
            
        # 处理所有到期的事件通知
        for event_data in events_to_trigger:
            try:
                print(f"提醒系统-通知管理器: {event_data['message']}")
                self.manager.notify(event_data)
            except Exception as e:
                print(f"通知管理器时出错: {e}")

    def check_reminder(self):
        now = datetime.now()
        # 从事件堆获取最近的事件
        with self.lock:
            if not self.event_heap.is_empty():
                next_event = self.event_heap.peek()
                event_time = datetime.fromtimestamp(next_event[0])
                
                if now >= event_time:
                    # 弹出事件并获取数据
                    _, event_data = self.event_heap.pop()
                    # 在主线程触发提醒
                    QTimer.singleShot(0, lambda: self.trigger_reminder(event_data))
        
        # 继续定时检查（保持原有逻辑）
        threading.Timer(1.0, self.check_reminder).start()

    
    def _calculate_sleep_time(self, now):
        """计算到下次事件的时间间隔"""
        with self.lock:
            if self.event_heap.is_empty():
                return 1.0
            
            next_event = self.event_heap.peek()
            if not next_event:
                return 1.0
            
            next_trigger = next_event[0]
        
        # 计算时间差
        time_diff = next_trigger - now
        
        # 根据不同时间间隔设置休眠时间
        if time_diff > 3600:    # 超过1小时
            return 10.0
        elif time_diff > 600:   # 10分钟以上
            return 1.0
        elif time_diff > 60:    # 1分钟以上
            return 0.5
        elif time_diff > 1:     # 1秒以上
            return 0.1
        else:
            return 0