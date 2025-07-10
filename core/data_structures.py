import threading
import time
import heapq

class Lock:
    """自定义互斥锁实现（自旋锁）"""
    def __init__(self):
        self._locked = False
    
    def acquire(self):
        """获取锁"""
        while True:
            if not self._locked:
                self._locked = True
                return
            time.sleep(0.001)  # 避免CPU占用过高
    
    def release(self):
        """释放锁"""
        self._locked = False

    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

class MinHeap:
    """自定义最小堆实现 - 核心数据结构"""
    def __init__(self):
        self._data = []  # 堆存储数组
        self.size = 0    # 堆大小
    
    def push(self, item):
        """向堆中插入元素"""
        heapq.heappush(self._data, item)
        self.size += 1
    
    def pop(self):
        """从堆中移除最小元素"""
        if self.size == 0:
            return None
        self.size -= 1
        return heapq.heappop(self._data)
    
    def peek(self):
        """查看堆顶元素"""
        if self.size == 0:
            return None
        return self._data[0]
    
    def is_empty(self):
        """检查堆是否为空"""
        return self.size == 0
    
    def __str__(self):
        """堆结构可视化"""
        if self.is_empty():
            return "Empty Heap"
        return str(self._data)

class ThreadSafeHeap:
    """线程安全的最小堆封装"""
    def __init__(self):
        self.heap = MinHeap()
        self.lock = Lock()  # 使用自定义锁
    
    def push(self, item):
        """线程安全的插入操作"""
        with self.lock:
            self.heap.push(item)
    
    def pop(self):
        """线程安全的删除最小元素"""
        with self.lock:
            return self.heap.pop()
    
    def peek(self):
        """线程安全的查看堆顶元素"""
        with self.lock:
            return self.heap.peek()
    
    def is_empty(self):
        """检查堆是否为空"""
        with self.lock:
            return self.heap.is_empty()