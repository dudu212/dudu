"""
@ File        : log_manager.py
@ Author      : 示例
@ Version     : V1.0.0
@ Description : 日志管理类，用于管理养花日志的添加、加载和保存操作
"""
import json
import os
from datetime import datetime


class LogEntry:
    """日志条目类，用于表示单条日志信息"""
    def __init__(self, plant_name, content, weather, growth,image,date=None):
        self.plant_name = plant_name
        self.content = content
        self.weather = weather
        self.growth = growth
        self.date = date if date else datetime.now()
        self.image = image

class LogManager:
    """日志管理类，负责日志的添加、加载和保存"""
    def __init__(self, log_file="logs.json"):
        self.log_file = log_file
        self.logs = []
        self.last_added = None
        self.load_from_file()

    def add_log(self, plant_name, content, weather=None, growth=None,image=None):
        """添加新的日志条目"""
        # image = image_path
        log_entry = LogEntry(plant_name, content, weather, growth,image)
        self.logs.append(log_entry)
        self.last_added = log_entry
        return log_entry

    def get_recent_logs(self, num=10):
        """获取最近的指定数量的日志"""
        return self.logs[-num:]

    def load_from_file(self):
        """从文件加载日志"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for entry in data:
                        log_entry = LogEntry(
                            entry['plant_name'],
                            entry['content'],
                            entry['weather'],
                            entry['growth'],
                            entry.get('image',None),
                            datetime.fromisoformat(entry['date'])
                        )
                        self.logs.append(log_entry)
            except Exception as e:
                print(f"加载日志文件时出错: {e}")

    def save_to_file(self):
        """保存日志到文件"""
        data = []
        for entry in self.logs:
            data.append({
                'plant_name': entry.plant_name,
                'content': entry.content,
                'weather': entry.weather,
                'growth': entry.growth,
                'date': entry.date.isoformat(),
                'image': entry.image
            })
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存日志文件时出错: {e}")