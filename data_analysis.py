# 模拟数据存储 - 扩展更多花卉和更详细的数据
# 模拟数据存储 - 扩展更多花卉和更详细的数据
flower_data = {
    "玫瑰": {
        "温度": {"optimal": "22°C", "interval": 3, "description": "适宜温暖环境"},
        "湿度": {"optimal": "60%", "interval": 4, "description": "需要中等湿度"},
        "光照": {"optimal": "6小时/天", "interval": 5, "description": "充足阳光"},
        "土壤PH值": {"optimal": "6.5", "interval": 4, "description": "弱酸性土壤"},
    },
    "百合": {
        "温度": {"optimal": "20°C", "interval": 5, "description": "偏好凉爽气候"},
        "湿度": {"optimal": "70%", "interval": 3, "description": "需要较高湿度"},
        "光照": {"optimal": "5小时/天", "interval": 4, "description": "半阴环境最佳"},
        "土壤PH值": {"optimal": "6.0", "interval": 6, "description": "中性土壤"},
    },
    "康乃馨": {
        "温度": {"optimal": "18°C", "interval": 4, "description": "较耐寒"},
        "湿度": {"optimal": "50%", "interval": 5, "description": "不宜过高湿度"},
        "光照": {"optimal": "7小时/天", "interval": 3, "description": "阳光充足促进开花"},
        "土壤PH值": {"optimal": "7.0", "interval": 5, "description": "中性土壤"},
    },
    "郁金香": {
        "温度": {"optimal": "15°C", "interval": 7, "description": "偏好冷凉环境"},
        "湿度": {"optimal": "55%", "interval": 6, "description": "湿度不宜过高"},
        "光照": {"optimal": "6小时/天", "interval": 8, "description": "充足阳光"},
        "土壤PH值": {"optimal": "7.0", "interval": 7, "description": "中性土壤"},
    },
}

def get_recommended_interval(flower_name):
    """获取推荐提醒间隔天数"""
    # 获取特定花卉的平均间隔时间
    if flower_name in flower_data:
        factors = flower_data[flower_name]
        total_interval = sum(data["interval"] for data in factors.values())
        avg_interval = round(total_interval / len(factors))
        return max(1, min(avg_interval, 30))  # 确保在合理范围内
    return 7  # 默认值

def analyze_flower_data(flower_name, factor):
    """分析花卉数据"""
    if flower_name in flower_data and factor in flower_data[flower_name]:
        return flower_data[flower_name][factor]
    return {"error": "未找到相关数据"}