import json
import os
from datetime import datetime
from dataclasses import dataclass, asdict
import pandas as pd
from typing import List, Dict, Optional

@dataclass
class LogEntry:
    """增强型日志条目类"""
    plant_name: str
    content: str
    weather: str
    growth_stage: str
    image: Optional[str] = None
    date: datetime = datetime.now()
    
    # 新增环境参数字段
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    light_intensity: Optional[int] = None
    soil_ph: Optional[float] = None
    water_interval: Optional[int] = None
    lifespan: Optional[int] = None

class LogManager:
    """支持数据分析的日志管理器"""
    def __init__(self, log_file="logs.json", data_file="flower_data.json"):
        self.log_file = log_file
        self.data_file = data_file
        self.logs: List[LogEntry] = []
        self.last_added: Optional[LogEntry] = None
        self.load_from_file()
        
    def add_log(self, 
               plant_name: str, 
               content: str, 
               weather: str, 
               growth_stage: str, 
               image: str = None,
               **env_params) -> LogEntry:
        """添加日志并自动补充环境数据"""
        log_entry = LogEntry(
            plant_name=plant_name,
            content=content,
            weather=weather,
            growth_stage=growth_stage,
            image=image,
            **env_params
        )
        
        # 自动生成模拟环境数据（实际应用应接入传感器）
        if not env_params:
            log_entry = self._generate_env_data(log_entry)
            
        self.logs.append(log_entry)
        self.last_added = log_entry
        self._update_analytics_data(log_entry)
        return log_entry

    def _generate_env_data(self, entry: LogEntry) -> LogEntry:
        """为日志生成模拟环境数据"""
        env_rules = {
            '晴': {'temp_range': (22, 30), 'humidity_range': (40, 60)},
            '多云': {'temp_range': (18, 25), 'humidity_range': (50, 70)},
            '雨': {'temp_range': (15, 22), 'humidity_range': (70, 90)}
        }
        
        rule = env_rules.get(entry.weather, env_rules['晴'])
        
        entry.temperature = round(
            random.uniform(*rule['temp_range']), 1
        )
        entry.humidity = round(
            random.uniform(*rule['humidity_range']), 1
        )
        entry.light_intensity = random.randint(1000, 3000)
        entry.soil_ph = round(random.uniform(5.5, 7.0), 1)
        entry.water_interval = random.randint(3, 7)
        entry.lifespan = random.randint(7, 21)
        
        return entry

    def _update_analytics_data(self, entry: LogEntry):
        """更新分析数据集"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
                
            plant_data = data.get(entry.plant_name, [])
            plant_data.append(asdict(entry))
            data[entry.plant_name] = plant_data[-100:]  # 保留最近100条
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=4, default=str)
        except Exception as e:
            print(f"更新分析数据失败: {e}")

    def get_analytics_data(self, plant_name: str) -> pd.DataFrame:
        """获取指定植物的分析数据"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f).get(plant_name, [])
            return pd.DataFrame(data)
        except FileNotFoundError:
            return pd.DataFrame()

    def load_from_file(self):
        """从文件加载日志（兼容旧格式）"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    raw_logs = json.load(f)
                    
                for entry in raw_logs:
                    self.logs.append(LogEntry(
                        plant_name=entry['plant_name'],
                        content=entry['content'],
                        weather=entry['weather'],
                        growth_stage=entry['growth'],
                        image=entry.get('image'),
                        date=datetime.fromisoformat(entry['date'])
                    ))
            except Exception as e:
                print(f"加载日志失败: {e}")

    def save_to_file(self):
        """保存日志（兼容旧格式）"""
        data = [{
            'plant_name': entry.plant_name,
            'content': entry.content,
            'weather': entry.weather,
            'growth': entry.growth_stage,
            'date': entry.date.isoformat(),
            'image': entry.image,
            **{k: v for k, v in asdict(entry).items() 
               if k not in ['plant_name', 'content', 'weather', 'growth_stage', 'date', 'image']}
        } for entry in self.logs]
        
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存日志失败: {e}")

    def get_recent_logs(self, num=10) -> List[LogEntry]:
        """获取最近N条日志"""
        return sorted(self.logs, key=lambda x: x.date)[-num:]