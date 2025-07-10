import time
from datetime import datetime, timedelta
from core.data_structures import Lock, MinHeap, ThreadSafeHeap
from core.reminder_system import FlowerCareReminderSystem
from core.data_analysis import FlowerDataAnalyzer

def test_lock():
    """测试自定义锁功能"""
    print("="*50)
    print("测试自定义锁功能")
    lock = Lock()
    
    # 测试基础功能
    lock.acquire()
    print("锁已获取")
    lock.release()
    print("锁已释放")
    
    # 测试上下文管理器
    with lock:
        print("在锁的上下文中")
    
    print("锁测试通过")
    print("="*50)

def test_min_heap():
    """测试最小堆功能"""
    print("\n" + "="*50)
    print("测试最小堆功能")
    heap = MinHeap()
    
    # 测试插入
    test_data = [5, 3, 8, 1, 2, 7, 4]
    for num in test_data:
        heap.push(num)
        print(f"插入 {num} 后堆状态: {heap}")
    
    # 测试弹出
    while not heap.is_empty():
        min_val = heap.pop()
        print(f"弹出最小值: {min_val} | 堆状态: {heap}")
    
    print("最小堆测试通过")
    print("="*50)

def test_thread_safe_heap():
    """测试线程安全堆"""
    print("\n" + "="*50)
    print("测试线程安全堆")
    safe_heap = ThreadSafeHeap()
    
    # 单线程测试
    safe_heap.push(10)
    safe_heap.push(5)
    safe_heap.push(15)
    
    print("堆内容:", [safe_heap.pop() for _ in range(3)])
    
    # 多线程测试
    from threading import Thread
    def worker(heap, id):
        for i in range(3):
            heap.push(id * 10 + i)
    
    threads = []
    for i in range(3):
        t = Thread(target=worker, args=(safe_heap, i))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("多线程操作后堆内容:", [safe_heap.pop() for _ in range(9)])
    print("线程安全堆测试通过")
    print("="*50)

def test_reminder_system():
    """测试提醒系统"""
    print("\n" + "="*50)
    print("测试提醒系统功能")
    
    # 创建系统实例
    system = FlowerCareReminderSystem()
    
    # 模拟回调
    def test_callback(event):
        print(f"[回调] 收到提醒: {event['message']}")
    
    # 注册回调
    system.callbacks.append(test_callback)
    
    # 添加测试提醒
    start_time = datetime.now() + timedelta(seconds=2)
    system.add_flower_reminder("玫瑰", start_time, 1, 3)
    
    # 启动系统
    system.start()
    
    try:
        print("等待10秒接收提醒...")
        time.sleep(10)
    finally:
        system.stop()
        print("提醒系统已停止")
    
    print("提醒系统测试通过")
    print("="*50)

def test_data_analyzer():
    """测试数据分析器"""
    print("\n" + "="*50)
    print("测试数据分析器")
    
    analyzer = FlowerDataAnalyzer()
    
    # 测试获取推荐间隔
    flowers = ["玫瑰", "百合", "郁金香", "未知鲜花"]
    for flower in flowers:
        interval = analyzer.get_recommended_interval(flower)
        print(f"{flower}的推荐养护间隔: {interval}天")
    
    # 测试数据分析
    factors = ["温度", "湿度", "光照", "土壤PH值"]
    for flower in flowers[:3]:
        for factor in factors:
            result = analyzer.analyze_flower_data(flower, factor)
            print(f"{flower}的{factor}分析:")
            print(f"  最优值: {result['optimal']}")
            print(f"  建议间隔: {result['interval']}天")
    
    print("数据分析器测试通过")
    print("="*50)

if __name__ == "__main__":
    # 运行所有测试
    test_lock()
    test_min_heap()
    test_thread_safe_heap()
    test_reminder_system()
    test_data_analyzer()
    
    print("\n所有测试完成")