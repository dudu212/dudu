import threading

class ThreadSafeMinHeap:
    """线程安全的最小堆实现（完全底层实现）"""
    
    def __init__(self):
        """初始化堆"""
        self._heap = []  # 使用数组存储堆元素
        self._lock = threading.Lock()  # 线程安全锁
    
    def push(self, item):
        """添加元素到堆中"""
        with self._lock:
            # 1. 将新元素添加到数组末尾
            self._heap.append(item)
            # 2. 执行上浮操作恢复堆性质
            self._sift_up(len(self._heap) - 1)
    
    def pop(self):
        """弹出最小元素"""
        with self._lock:
            if not self._heap:
                return None
            
            # 1. 保存堆顶元素（最小值）
            min_val = self._heap[0]
            
            # 2. 将最后一个元素移到堆顶
            last = self._heap.pop()
            if self._heap:
                self._heap[0] = last
                # 3. 执行下沉操作恢复堆性质
                self._sift_down(0)
            
            return min_val
    
    def peek(self):
        """查看最小元素但不弹出"""
        with self._lock:
            return self._heap[0] if self._heap else None
    
    def is_empty(self):
        """检查堆是否为空"""
        with self._lock:
            return len(self._heap) == 0
    
    def __len__(self):
        """获取堆中元素数量"""
        with self._lock:
            return len(self._heap)
    
    def _sift_up(self, index):
        """上浮操作：将元素向上调整到正确位置"""
        # 当元素不是根节点且小于其父节点时，持续上浮
        while index > 0:
            parent_index = (index - 1) // 2
            
            # 如果当前节点大于等于父节点，堆性质已满足
            if self._heap[index] >= self._heap[parent_index]:
                break
            
            # 交换当前节点与父节点
            self._heap[index], self._heap[parent_index] = \
                self._heap[parent_index], self._heap[index]
            
            # 更新索引为父节点位置
            index = parent_index
    
    def _sift_down(self, index):
        """下沉操作：将元素向下调整到正确位置"""
        size = len(self._heap)
        
        # 循环直到没有子节点
        while True:
            smallest = index
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            
            # 检查左子节点是否存在且小于当前节点
            if left_child < size and self._heap[left_child] < self._heap[smallest]:
                smallest = left_child
            
            # 检查右子节点是否存在且小于当前节点
            if right_child < size and self._heap[right_child] < self._heap[smallest]:
                smallest = right_child
            
            # 如果当前节点小于等于子节点，堆性质已满足
            if smallest == index:
                break
            
            # 交换当前节点与最小子节点
            self._heap[index], self._heap[smallest] = \
                self._heap[smallest], self._heap[index]
            
            # 更新索引为子节点位置
            index = smallest
    
    def heapify(self, items):
        """堆化操作：将无序列表转换为最小堆"""
        with self._lock:
            self._heap = items.copy()
            # 从最后一个非叶子节点开始向前执行下沉操作
            # 最后一个非叶子节点的索引 = 最后一个元素的父节点索引
            start_index = (len(self._heap) - 2) // 2
            for i in range(start_index, -1, -1):
                self._sift_down(i)
    
    def __str__(self):
        """可视化堆结构"""
        with self._lock:
            if not self._heap:
                return "Empty Heap"
            
            # 计算堆的层级
            levels = []
            level = 0
            current_level = []
            
            for i, val in enumerate(self._heap):
                current_level.append(str(val))
                # 当当前层填满时（2^level个元素）
                if i == (1 << level) - 1:
                    levels.append("  ".join(current_level))
                    current_level = []
                    level += 1
            
            if current_level:
                levels.append("  ".join(current_level))
            
            # 居中对齐每层元素
            max_width = len(levels[-1])
            result = []
            for i, level_str in enumerate(levels):
                padding = (max_width - len(level_str)) // 2
                result.append(" " * padding + level_str)
            
            return "\n".join(result)


# 测试最小堆功能
if __name__ == "__main__":
    print("=== 最小堆功能测试 ===")
    heap = ThreadSafeMinHeap()
    
    # 添加元素
    test_data = [5, 3, 8, 1, 2, 7, 4, 6]
    print(f"添加元素: {test_data}")
    for num in test_data:
        heap.push(num)
    
    # 可视化堆结构
    print("\n堆结构:")
    print(heap)
    
    # 弹出元素
    print("\n弹出元素:")
    while not heap.is_empty():
        print(f"弹出最小值: {heap.pop()}  剩余元素: {[heap._heap[i] for i in range(len(heap))]}")
    
    # 堆化测试
    print("\n=== 堆化功能测试 ===")
    heap = ThreadSafeMinHeap()
    heap.heapify([9, 5, 2, 7, 1, 6, 8, 3])
    print("堆化后的结构:")
    print(heap)
    
    # 多线程安全测试
    print("\n=== 多线程安全测试 ===")
    import concurrent.futures
    
    heap = ThreadSafeMinHeap()
    
    def worker_push(items):
        for item in items:
            heap.push(item)
    
    def worker_pop(count):
        for _ in range(count):
            heap.pop()
    
    # 创建多个线程同时操作堆
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # 两个线程添加元素
        executor.submit(worker_push, [10, 20, 15, 5])
        executor.submit(worker_push, [25, 3, 8, 12])
        # 两个线程弹出元素
        executor.submit(worker_pop, 3)
        executor.submit(worker_pop, 2)
    
    # 打印最终堆状态
    print("多线程操作后堆状态:")
    print(heap)
    print(f"剩余元素数量: {len(heap)}")