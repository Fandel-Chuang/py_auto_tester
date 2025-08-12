"""
命令行接口模块
"""

import argparse
import sys
import os
from .core import AutoTester


def main():
    """
    命令行入口函数
    """
    parser = argparse.ArgumentParser(
        description="Python自动化单元测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  py-auto-tester                    # 在当前目录的tests文件夹中运行所有测试
  py-auto-tester --dir mytests      # 在mytests目录中运行测试
  py-auto-tester --template MyClass # 为MyClass生成测试模板
  py-auto-tester --coverage        # 运行测试并生成覆盖率报告
        """
    )
    
    parser.add_argument(
        "--dir", "-d",
        default="tests",
        help="测试文件所在目录 (默认: tests)"
    )
    
    parser.add_argument(
        "--pattern", "-p",
        default="test_*.py",
        help="测试文件匹配模式 (默认: test_*.py)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细输出"
    )
    
    parser.add_argument(
        "--template", "-t",
        help="为指定类名生成测试模板"
    )
    
    parser.add_argument(
        "--from-file", "-f",
        help="从指定源文件读取类和函数，根据docstring生成测试文件"
    )
    
    parser.add_argument(
        "--class-filter",
        help="只为指定类生成测试（与--from-file一起使用）"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="测试模板或生成的测试文件输出路径"
    )
    
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="显示测试覆盖率信息"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="py_auto_tester 0.2.0 (支持Python 3.7-3.12)"
    )
    
    args = parser.parse_args()
    
    # 创建AutoTester实例
    tester = AutoTester(
        test_directory=args.dir,
        pattern=args.pattern
    )
    
    try:
        # 从文件生成测试
        if args.from_file:
            print(f"正在从源文件生成测试: {args.from_file}")
            try:
                test_code = tester.generate_test_from_file(
                    source_file=args.from_file,
                    output_file=args.output,
                    class_filter=args.class_filter
                )
                if not args.output:
                    print("生成的测试代码:")
                    print("-" * 50)
                    print(test_code)
                return 0
            except Exception as e:
                print(f"生成测试时发生错误: {e}")
                return 1
        
        # 生成测试模板
        if args.template:
            template = tester.generate_test_template(
                class_name=args.template,
                output_file=args.output
            )
            if not args.output:
                print("生成的测试模板:")
                print("-" * 50)
                print(template)
            return 0
        
        # 发现测试文件
        print(f"正在搜索测试文件: {args.dir}")
        discovered = tester.discover_tests()
        
        if not discovered:
            print(f"在目录 '{args.dir}' 中未找到测试文件")
            print("请确保:")
            print("1. 测试目录存在")
            print("2. 测试文件以 'test_' 开头并以 '.py' 结尾")
            return 1
        
        print(f"发现 {len(discovered)} 个测试文件:")
        for test_file in discovered:
            print(f"  - {test_file}")
        print()
        
        # 运行测试
        print("运行测试...")
        print("=" * 60)
        
        results = tester.run_tests(verbose=args.verbose)
        
        print("=" * 60)
        print("测试结果统计:")
        print(f"  总计: {results['total']}")
        print(f"  通过: {results['passed']}")
        print(f"  失败: {results['failed']}")
        print(f"  错误: {results['errors']}")
        
        # 显示覆盖率信息
        if args.coverage:
            print("\n" + "=" * 60)
            coverage_info = tester.get_test_coverage()
            if coverage_info['coverage_available']:
                print("覆盖率信息:")
                print(coverage_info['message'])
            else:
                print("覆盖率信息不可用:")
                print(coverage_info['message'])
        
        # 返回适当的退出代码
        if results['failed'] > 0 or results['errors'] > 0:
            return 1
        else:
            return 0
            
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        return 130
    except Exception as e:
        print(f"运行测试时发生错误: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())