from collections import defaultdict, deque
import random

class FlowerDataAnalyzer:
    """鲜花数据智能分析器 - 使用多种数据结构实现推荐算法"""
    def __init__(self):
        # 历史数据存储结构
        self.history = defaultdict(list)  # {flower: [interval_days]}
        self.recent_entries = deque(maxlen=100)  # 最近100条记录
        
        # 初始化模拟数据
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """初始化样本数据"""
        flowers = ["玫瑰", "百合", "郁金香", "康乃馨", "向日葵", "满天星"]
        for flower in flowers:
            for _ in range(20):
                interval = random.randint(3, 10)
                self.add_data_point(flower, interval)
    
    def add_data_point(self, flower, interval_days):
        """添加新的数据点"""
        self.history[flower].append(interval_days)
        self.recent_entries.append((flower, interval_days))
    
    def get_recommended_interval(self, flower):
        """获取推荐间隔天数 - 使用多种算法组合"""
        # 1. 基于该鲜花的历史数据（加权平均）
        if flower in self.history and len(self.history[flower]) >= 3:
            data = self.history[flower]
            # 使用最近3个数据的平均值
            recent_data = data[-3:]
            return round(sum(recent_data) / len(recent_data), 1)
        else:
            # 数据不足时使用全局平均
            return self._get_global_avg()
    
    def _get_global_avg(self):
        """获取全局平均间隔"""
        if not self.recent_entries:
            return 7.0  # 默认值
        
        total = sum(interval for _, interval in self.recent_entries)
        return round(total / len(self.recent_entries), 1)
    
    def analyze_flower_data(self, flower, factor):
        """分析鲜花数据（用于数据分析界面）"""
        # 生成随机浮点数
        def rand_float(a, b):
            return round(random.uniform(a, b), 1)
        
        # 生成随机整数
        def rand_int(a, b):
            return random.randint(a, b)
        
        optimal_value = {
            "温度": f"{rand_float(18, 25)}°C",
            "湿度": f"{rand_float(50, 80)}%",
            "光照": f"{rand_int(1000, 3000)} lux",
            "土壤PH值": f"{rand_float(5.5, 7.0)}"
        }.get(factor, "N/A")
        
        return {
            "optimal": optimal_value,
            "interval": self.get_recommended_interval(flower),
            "factors": {
                "温度": rand_float(18, 25),
                "湿度": rand_float(50, 80),
                "光照": rand_int(1000, 3000),
                "土壤PH值": rand_float(5.5, 7.0)
            }
        }