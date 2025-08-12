"""
核心自动化测试类
"""

import unittest
import os
import sys
import importlib.util
from typing import List, Optional, Dict, Any
import inspect
import ast
import re



class AutoTester:
    """
    Python自动化单元测试工具的核心类
    
    用于自动发现、执行和报告Python项目中的单元测试。
    """
    
    def __init__(self, test_directory: str = "tests", pattern: str = "test_*.py"):
        """
        初始化AutoTester
        
        Args:
            test_directory: 测试文件所在目录，默认为"tests"
            pattern: 测试文件的命名模式，默认为"test_*.py"
        """
        self.test_directory = test_directory
        self.pattern = pattern
        self.discovered_tests = []
        
    def discover_tests(self) -> List[str]:
        """
        自动发现测试文件
        
        Returns:
            发现的测试文件列表
        """
        test_files = []
        
        if not os.path.exists(self.test_directory):
            print(f"警告: 测试目录 '{self.test_directory}' 不存在")
            return test_files
            
        for root, dirs, files in os.walk(self.test_directory):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    test_files.append(os.path.join(root, file))
                    
        self.discovered_tests = test_files
        return test_files
    
    def run_tests(self, verbose: bool = True) -> Dict[str, Any]:
        """
        运行发现的测试
        
        Args:
            verbose: 是否显示详细输出
            
        Returns:
            测试结果统计信息
        """
        if not self.discovered_tests:
            self.discover_tests()
            
        if not self.discovered_tests:
            return {"total": 0, "passed": 0, "failed": 0, "errors": 0}
            
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # 加载所有测试
        for test_file in self.discovered_tests:
            try:
                # 将文件路径转换为模块名
                module_name = os.path.splitext(os.path.basename(test_file))[0]
                spec = importlib.util.spec_from_file_location(module_name, test_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # 加载测试用例
                tests = loader.loadTestsFromModule(module)
                suite.addTests(tests)
                
            except Exception as e:
                print(f"加载测试文件 {test_file} 时出错: {e}")
                
        # 运行测试
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(suite)
        
        return {
            "total": result.testsRun,
            "passed": result.testsRun - len(result.failures) - len(result.errors),
            "failed": len(result.failures),
            "errors": len(result.errors),
            "failures": result.failures,
            "error_details": result.errors
        }
    
    def generate_test_template(self, class_name: str, output_file: Optional[str] = None) -> str:
        """
        生成测试模板
        
        Args:
            class_name: 要测试的类名
            output_file: 输出文件路径，如果为None则返回模板字符串
            
        Returns:
            测试模板字符串
        """
        template = f'''"""
{class_name}的单元测试
"""

import unittest
from unittest.mock import Mock, patch


class Test{class_name}(unittest.TestCase):
    """
    {class_name}类的测试用例
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        pass
        
    def tearDown(self):
        """
        测试后的清理
        """
        pass
    
    def test_example(self):
        """
        示例测试用例
        """
        # TODO: 实现具体的测试逻辑
        self.assertTrue(True)
        
    def test_another_example(self):
        """
        另一个示例测试用例
        """
        # TODO: 实现具体的测试逻辑
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()
'''
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(template)
            print(f"测试模板已生成: {output_file}")
            
        return template
    
    def generate_test_from_file(self, source_file: str, output_file: Optional[str] = None, 
                               class_filter: Optional[str] = None) -> str:
        """
        从源文件读取类和函数，根据函数注释中的测试用例生成测试文件
        
        Args:
            source_file: 源代码文件路径
            output_file: 输出测试文件路径，如果为None则返回测试代码字符串
            class_filter: 只为指定类生成测试，如果为None则为所有类生成测试
            
        Returns:
            生成的测试代码字符串
        """
        if not os.path.exists(source_file):
            raise FileNotFoundError(f"源文件不存在: {source_file}")
            
        # 解析源文件
        with open(source_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
            
        # 解析AST
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            raise SyntaxError(f"源文件语法错误: {e}")
        
        # 提取类和函数信息
        classes_info = self._extract_classes_and_functions(tree, source_code)
        
        # 过滤类
        if class_filter:
            classes_info = {k: v for k, v in classes_info.items() if k == class_filter}
            
        if not classes_info:
            if class_filter:
                raise ValueError(f"在文件 {source_file} 中未找到类 {class_filter}")
            else:
                raise ValueError(f"在文件 {source_file} 中未找到任何类")
        
        # 生成测试代码
        test_code = self._generate_test_code_from_classes(classes_info, source_file)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(test_code)
            print(f"测试文件已生成: {output_file}")
            
        return test_code
    
    def _extract_classes_and_functions(self, tree: ast.AST, source_code: str) -> Dict[str, Dict]:
        """
        从AST中提取类和函数信息
        
        Args:
            tree: AST树
            source_code: 源代码字符串
            
        Returns:
            包含类和函数信息的字典
        """
        classes_info = {}
        source_lines = source_code.split('\n')
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name
                methods_info = {}
                
                # 遍历类中的方法
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_name = item.name
                        
                        # 获取函数的docstring
                        docstring = ast.get_docstring(item)
                        if docstring:
                            # 解析docstring中的测试用例
                            test_cases = self._parse_docstring_test_cases(docstring)
                            if test_cases:
                                methods_info[method_name] = {
                                    'docstring': docstring,
                                    'test_cases': test_cases,
                                    'line_number': item.lineno
                                }
                
                if methods_info:
                    classes_info[class_name] = {
                        'methods': methods_info,
                        'line_number': node.lineno
                    }
        
        return classes_info
    
    def _parse_docstring_test_cases(self, docstring: str) -> List[Dict[str, Any]]:
        """
        解析docstring中的测试用例
        
        支持的格式:
        (args) -> expected_result
        (args) -> (expected_result && attr=value && method()=result)
        (args) -> expected_result @attr=init_value @method()=check_value
        
        Args:
            docstring: 函数的docstring
            
        Returns:
            测试用例列表
        """
        if not docstring:
            return []
            
        test_cases = []
        lines = docstring.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
                
            # 匹配测试用例格式: (args) -> (result && checks) @inits
            match = re.match(r'\s*\((.*?)\)\s*->\s*\(([^)]+)\)\s*((?:@[^@&]+)*)', line)
            if not match:
                # 尝试简单格式: (args) -> result
                simple_match = re.match(r'\s*\((.*?)\)\s*->\s*([^@#]+?)(?:\s*[@#]|$)', line)
                if simple_match:
                    inputs_str, result_str = simple_match.groups()
                    match = (inputs_str, result_str.strip(), '')
                else:
                    continue
            else:
                inputs_str, output_and_checks, init_part = match.groups()
                match = (inputs_str, output_and_checks, init_part)
            
            if match:
                inputs_str, output_str, init_part = match
                
                # 解析输入参数
                test_case = self._parse_test_inputs(inputs_str)
                test_case['line_number'] = line_num
                test_case['raw_line'] = line
                
                # 解析输出和检查
                if '&&' in output_str:
                    # 复杂格式: result && attr=value
                    parts = output_str.split('&&')
                    # 第一部分是返回值
                    test_case['expected'] = self._parse_test_value(parts[0].strip())
                    
                    # 其余部分是属性检查
                    test_case['check_attrs'] = {}
                    for part in parts[1:]:
                        if '=' in part:
                            attr, value = part.split('=', 1)
                            test_case['check_attrs'][attr.strip()] = self._parse_test_value(value.strip())
                else:
                    # 简单格式: 只有返回值
                    test_case['expected'] = self._parse_test_value(output_str.strip())
                
                # 解析初始属性设置 (@attr=value)
                if init_part:
                    init_attrs = re.findall(r'@\s*([^=\s@&]+(?:\([^)]*\))?(?:\[[^\]]*\])*)\s*=\s*([^@&]+?)(?=\s*[@&]|$)', init_part)
                    if init_attrs:
                        test_case['init_attrs'] = {}
                        for attr, value in init_attrs:
                            test_case['init_attrs'][attr.strip()] = self._parse_test_value(value.strip())
                
                test_cases.append(test_case)
        
        return test_cases
    
    def _parse_test_inputs(self, inputs_str: str) -> Dict[str, Any]:
        """
        解析测试用例的输入参数
        
        Args:
            inputs_str: 输入参数字符串
            
        Returns:
            包含解析结果的字典
        """
        test_case = {}
        
        if not inputs_str.strip():
            test_case['inputs'] = ()
            return test_case
        
        try:
            # 尝试直接解析为字面值
            params = ast.literal_eval(f"({inputs_str},)" if inputs_str else "()")
            if not isinstance(params, tuple):
                params = (params,)
            test_case['inputs'] = params
        except (SyntaxError, ValueError):
            # 如果包含动态表达式，保存原始字符串，在运行时动态求值
            test_case['inputs'] = f"({inputs_str},)" if inputs_str else "()"
            test_case['dynamic_inputs'] = True
        
        return test_case
    
    def _parse_test_value(self, value_str: str) -> Any:
        """
        解析测试值
        
        Args:
            value_str: 值字符串
            
        Returns:
            解析后的值
        """
        value_str = value_str.strip()
        
        if not value_str:
            return None
            
        # 处理类型检查格式: type:int
        if value_str.startswith('type:'):
            return value_str
        
        try:
            # 尝试解析为字面值
            return ast.literal_eval(value_str)
        except (SyntaxError, ValueError):
            # 如果不是字面值，返回原始字符串
            return value_str
    
    def _generate_test_code_from_classes(self, classes_info: Dict[str, Dict], source_file: str) -> str:
        """
        根据类信息生成测试代码
        
        Args:
            classes_info: 类信息字典
            source_file: 源文件路径
            
        Returns:
            生成的测试代码
        """
        # 获取源文件的模块名
        module_name = os.path.splitext(os.path.basename(source_file))[0]
        
        # 生成导入语句
        imports = f'''"""
从 {source_file} 自动生成的测试文件
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# 添加源文件路径到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath('{source_file}')))

# 导入被测试的模块
try:
    from {module_name} import *
except ImportError as e:
    print(f"导入模块失败: {{e}}")
    # 尝试其他导入方式
    import importlib.util
    spec = importlib.util.spec_from_file_location("{module_name}", "{source_file}")
    {module_name}_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module({module_name}_module)
    globals().update(vars({module_name}_module))

'''
        
        # 为每个类生成测试
        test_classes = []
        for class_name, class_info in classes_info.items():
            test_class_code = self._generate_test_class_code(class_name, class_info)
            test_classes.append(test_class_code)
        
        # 组合完整的测试代码
        full_test_code = imports + '\n\n'.join(test_classes) + '''

if __name__ == '__main__':
    unittest.main()
'''
        
        return full_test_code
    
    def _generate_test_class_code(self, class_name: str, class_info: Dict) -> str:
        """
        为单个类生成测试代码
        
        Args:
            class_name: 类名
            class_info: 类信息
            
        Returns:
            类的测试代码
        """
        test_methods = []
        
        for method_name, method_info in class_info['methods'].items():
            test_method_code = self._generate_test_method_code(
                class_name, method_name, method_info['test_cases']
            )
            test_methods.append(test_method_code)
        
        test_class_template = f'''class Test{class_name}(unittest.TestCase):
    """
    {class_name}类的自动生成测试用例
    """
    
    def setUp(self):
        """
        测试前的设置
        """
        self.test_obj = {class_name}()
    
    def tearDown(self):
        """
        测试后的清理
        """
        pass

{chr(10).join(test_methods)}'''
        
        return test_class_template
    
    def _generate_test_method_code(self, class_name: str, method_name: str, test_cases: List[Dict]) -> str:
        """
        为单个方法生成测试代码
        
        Args:
            class_name: 类名
            method_name: 方法名
            test_cases: 测试用例列表
            
        Returns:
            方法的测试代码
        """
        if not test_cases:
            return ""
        
        test_code_parts = []
        
        for i, test_case in enumerate(test_cases):
            case_num = i + 1
            
            # 生成测试用例代码
            case_code = f'''
        # 测试用例 {case_num}: {test_case.get('raw_line', '')}
        '''
            
            # 设置初始属性
            if test_case.get('init_attrs'):
                case_code += '''
        # 设置初始属性'''
                for attr, value in test_case['init_attrs'].items():
                    case_code += f'''
        # TODO: 设置 {attr} = {value}'''
            
            # 调用方法
            if test_case.get('dynamic_inputs'):
                case_code += f'''
        # 动态输入参数: {test_case['inputs']}
        # TODO: 实现动态参数解析
        result = self.test_obj.{method_name}()  # 请根据实际情况调整参数'''
            else:
                inputs = test_case.get('inputs', ())
                if inputs:
                    args_str = ', '.join(repr(arg) for arg in inputs)
                    case_code += f'''
        result = self.test_obj.{method_name}({args_str})'''
                else:
                    case_code += f'''
        result = self.test_obj.{method_name}()'''
            
            # 检查返回值
            if 'expected' in test_case:
                expected = test_case['expected']
                if isinstance(expected, str) and expected.startswith('type:'):
                    type_name = expected[5:].strip()
                    case_code += f'''
        # 检查返回值类型
        self.assertIsInstance(result, {type_name}, f"用例{case_num}: 期望类型 {type_name}, 实际得到 {{type(result).__name__}}")'''
                else:
                    case_code += f'''
        # 检查返回值
        self.assertEqual(result, {repr(expected)}, f"用例{case_num}: 期望 {repr(expected)}, 实际得到 {{result}}")'''
            
            # 检查属性
            if test_case.get('check_attrs'):
                case_code += '''
        # 检查属性值'''
                for attr, expected_value in test_case['check_attrs'].items():
                    case_code += f'''
        # TODO: 检查属性 {attr} = {expected_value}
        # actual_value = getattr(self.test_obj, '{attr}', None)
        # self.assertEqual(actual_value, {repr(expected_value)}, f"用例{case_num}: 期望属性{attr}={repr(expected_value)}, 实际得到 {{actual_value}}")'''
            
            test_code_parts.append(case_code)
        
        # 组合所有测试用例
        all_cases_code = ''.join(test_code_parts)
        
        method_template = f'''    def test_{method_name}(self):
        """
        测试 {method_name} 方法 - 基于docstring自动生成
        """
        {all_cases_code}
        '''
        
        return method_template
    
    def get_test_coverage(self) -> Dict[str, Any]:
        """
        获取测试覆盖率信息（需要安装coverage包）
        
        Returns:
            覆盖率信息字典
        """
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()
            
            # 运行测试
            self.run_tests(verbose=False)
            
            cov.stop()
            cov.save()
            
            # 获取覆盖率报告
            return {"coverage_available": True, "message": "使用coverage.py查看详细报告"}
            
        except ImportError:
            return {"coverage_available": False, "message": "请安装coverage包以获取覆盖率信息"}