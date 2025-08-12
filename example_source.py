"""
示例源文件 - 用于演示自动测试生成功能
"""


class Calculator:
    """
    简单的计算器类
    """
    
    def __init__(self):
        self.result = 0
        
    def add(self, a, b):
        """
        加法运算
        
        测试用例：
        (1, 2) -> 3
        (0, 0) -> 0
        (-1, 1) -> 0
        (10, -5) -> 5
        """
        return a + b
        
    def subtract(self, a, b):
        """
        减法运算
        
        测试用例：
        (5, 3) -> 2
        (0, 0) -> 0
        (10, 15) -> -5
        """
        return a - b
        
    def multiply(self, a, b):
        """
        乘法运算
        
        测试用例：
        (3, 4) -> 12
        (0, 5) -> 0
        (-2, 3) -> -6
        """
        return a * b
        
    def divide(self, a, b):
        """
        除法运算
        
        测试用例：
        (10, 2) -> 5.0
        (7, 2) -> 3.5
        (0, 1) -> 0.0
        """
        if b == 0:
            raise ValueError("除数不能为零")
        return a / b
        
    def power(self, base, exponent):
        """
        幂运算
        
        测试用例：
        (2, 3) -> 8
        (5, 0) -> 1
        (3, 2) -> 9
        """
        return base ** exponent


class StringProcessor:
    """
    字符串处理器类
    """
    
    def __init__(self):
        self.processed_count = 0
        
    def reverse_string(self, text):
        """
        反转字符串
        
        测试用例：
        ("hello") -> "olleh"
        ("") -> ""
        ("a") -> "a"
        ("12345") -> "54321"
        """
        self.processed_count += 1
        return text[::-1]
        
    def count_words(self, text):
        """
        统计单词数量
        
        测试用例：
        ("hello world") -> 2
        ("") -> 0
        ("   ") -> 0
        ("one") -> 1
        ("a b c d e") -> 5
        """
        self.processed_count += 1
        if not text.strip():
            return 0
        return len(text.strip().split())
        
    def to_upper_case(self, text):
        """
        转换为大写
        
        测试用例：
        ("hello") -> "HELLO"
        ("") -> ""
        ("MiXeD cAsE") -> "MIXED CASE"
        """
        self.processed_count += 1
        return text.upper()


class ComplexExample:
    """
    复杂示例类 - 演示更高级的测试用例格式
    """
    
    def __init__(self):
        self.value = 0
        self.history = []
        
    def process_with_state(self, input_value):
        """
        带状态变化的处理方法
        
        测试用例：
        (5) -> (5 && value=5 && len(history)=1) @value=0 @history=[]
        (10) -> (10 && value=10 && len(history)=1) @value=3 @history=[1,2]
        """
        self.value = input_value
        self.history.append(input_value)
        return input_value
        
    def get_summary(self):
        """
        获取摘要信息
        
        测试用例：
        () -> type:dict
        () -> {'value': 5, 'count': 1} @value=5 @history=[10]
        """
        return {
            'value': self.value,
            'count': len(self.history)
        }