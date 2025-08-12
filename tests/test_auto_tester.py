"""
py_auto_tester 包的示例测试文件
"""

import unittest
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from py_auto_tester import AutoTester


class TestAutoTester(unittest.TestCase):
    """
    AutoTester类的测试用例
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        self.tester = AutoTester()
        
    def tearDown(self):
        """
        测试后的清理
        """
        pass
    
    def test_init(self):
        """
        测试AutoTester初始化
        """
        tester = AutoTester()
        self.assertEqual(tester.test_directory, "tests")
        self.assertEqual(tester.pattern, "test_*.py")
        self.assertEqual(tester.discovered_tests, [])
        
    def test_init_with_params(self):
        """
        测试带参数的AutoTester初始化
        """
        tester = AutoTester(test_directory="my_tests", pattern="*_test.py")
        self.assertEqual(tester.test_directory, "my_tests")
        self.assertEqual(tester.pattern, "*_test.py")
    
    def test_generate_test_template(self):
        """
        测试模板生成功能
        """
        template = self.tester.generate_test_template("MyClass")
        
        # 检查模板是否包含预期内容
        self.assertIn("class TestMyClass", template)
        self.assertIn("import unittest", template)
        self.assertIn("def setUp", template)
        self.assertIn("def tearDown", template)
        self.assertIn("def test_example", template)
    
    def test_discover_tests_nonexistent_directory(self):
        """
        测试在不存在的目录中发现测试文件
        """
        tester = AutoTester(test_directory="nonexistent_dir")
        tests = tester.discover_tests()
        self.assertEqual(tests, [])


if __name__ == '__main__':
    unittest.main()