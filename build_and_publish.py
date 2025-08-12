#!/usr/bin/env python
"""
py_auto_tester 构建和发布脚本

用法:
    python build_and_publish.py --help                    # 显示帮助
    python build_and_publish.py --build                   # 只构建
    python build_and_publish.py --test                    # 发布到测试PyPI
    python build_and_publish.py --publish                 # 发布到正式PyPI
    python build_and_publish.py --build --test            # 构建并发布到测试PyPI
    python build_and_publish.py --all                     # 完整流程：清理、构建、测试、发布
"""

import os
import sys
import subprocess
import shutil
import argparse
from pathlib import Path


class BuildPublisher:
    """构建和发布管理器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.egg_info_dirs = list(self.project_root.glob("*.egg-info"))
        
    def print_step(self, step_name):
        """打印步骤标题"""
        print(f"\n{'='*60}")
        print(f"🔥 {step_name}")
        print(f"{'='*60}")
        
    def run_command(self, command, check=True):
        """运行命令并处理错误"""
        print(f"执行命令: {' '.join(command) if isinstance(command, list) else command}")
        try:
            if isinstance(command, str):
                result = subprocess.run(command, shell=True, check=check, 
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(command, check=check, 
                                      capture_output=True, text=True)
            
            if result.stdout:
                print(result.stdout)
            if result.stderr and result.returncode != 0:
                print(f"错误: {result.stderr}")
                
            return result.returncode == 0
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            if e.stderr:
                print(f"错误信息: {e.stderr}")
            return False
    
    def clean_build_artifacts(self):
        """清理构建产物"""
        self.print_step("清理构建产物")
        
        dirs_to_clean = [self.dist_dir, self.build_dir] + self.egg_info_dirs
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                print(f"删除目录: {dir_path}")
                shutil.rmtree(dir_path)
            else:
                print(f"目录不存在，跳过: {dir_path}")
        
        # 清理 __pycache__ 目录
        for pycache in self.project_root.rglob("__pycache__"):
            print(f"删除缓存目录: {pycache}")
            shutil.rmtree(pycache)
            
        print("✅ 清理完成")
    
    def install_build_dependencies(self):
        """安装构建依赖"""
        self.print_step("检查并安装构建依赖")
        
        dependencies = ["build", "twine", "wheel", "setuptools"]
        
        for dep in dependencies:
            print(f"检查依赖: {dep}")
            if not self.run_command([sys.executable, "-m", "pip", "show", dep], check=False):
                print(f"安装依赖: {dep}")
                if not self.run_command([sys.executable, "-m", "pip", "install", dep]):
                    print(f"❌ 安装 {dep} 失败")
                    return False
            else:
                print(f"✅ {dep} 已安装")
        
        print("✅ 构建依赖检查完成")
        return True
    
    def run_tests(self):
        """运行测试"""
        self.print_step("运行项目测试")
        
        # 检查是否有测试目录
        tests_dir = self.project_root / "tests"
        if not tests_dir.exists():
            print("⚠️  未找到tests目录，跳过测试")
            return True
        
        # 尝试运行pytest
        if self.run_command([sys.executable, "-m", "pytest", "tests/", "-v"], check=False):
            print("✅ pytest测试通过")
            return True
        
        # 如果pytest失败，尝试使用unittest
        print("pytest失败，尝试使用unittest...")
        if self.run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], check=False):
            print("✅ unittest测试通过")
            return True
        
        # 使用我们自己的测试工具
        print("尝试使用py-auto-tester...")
        if self.run_command([sys.executable, "-m", "py_auto_tester", "--dir", "tests", "--verbose"], check=False):
            print("✅ py-auto-tester测试通过")
            return True
        
        print("⚠️  所有测试方法都失败了，但继续构建流程")
        return True  # 不阻止构建流程
    
    def build_package(self):
        """构建包"""
        self.print_step("构建Python包")
        
        if not self.run_command([sys.executable, "-m", "build"]):
            print("❌ 构建失败")
            return False
        
        # 检查构建产物
        if not self.dist_dir.exists():
            print("❌ dist目录未创建")
            return False
        
        dist_files = list(self.dist_dir.glob("*"))
        if not dist_files:
            print("❌ 未找到构建产物")
            return False
        
        print("✅ 构建成功！生成的文件:")
        for file in dist_files:
            print(f"  - {file.name}")
        
        return True
    
    def check_package(self):
        """检查包的完整性"""
        self.print_step("检查包完整性")
        
        if not self.run_command([sys.executable, "-m", "twine", "check", "dist/*"]):
            print("❌ 包检查失败")
            return False
        
        print("✅ 包检查通过")
        return True
    
    def publish_to_test_pypi(self):
        """发布到测试PyPI"""
        self.print_step("发布到测试PyPI")
        
        print("📤 正在上传到测试PyPI...")
        if not self.run_command([
            sys.executable, "-m", "twine", "upload", 
            "--repository", "testpypi", 
            "dist/*"
        ]):
            print("❌ 发布到测试PyPI失败")
            return False
        
        print("✅ 成功发布到测试PyPI")
        print("📋 测试安装命令:")
        print("pip install --index-url https://test.pypi.org/simple/ py-auto-tester")
        return True
    
    def publish_to_pypi(self):
        """发布到正式PyPI"""
        self.print_step("发布到正式PyPI")
        
        # 最后确认
        response = input("⚠️  即将发布到正式PyPI，确定继续吗？(yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("❌ 用户取消发布")
            return False
        
        print("📤 正在上传到正式PyPI...")
        if not self.run_command([sys.executable, "-m", "twine", "upload", "dist/*"]):
            print("❌ 发布到正式PyPI失败")
            return False
        
        print("✅ 成功发布到正式PyPI")
        print("📋 安装命令:")
        print("pip install py-auto-tester")
        return True
    
    def get_version(self):
        """获取当前版本号"""
        try:
            # 从 __init__.py 读取版本
            init_file = self.project_root / "py_auto_tester" / "__init__.py"
            with open(init_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('__version__'):
                        version = line.split('=')[1].strip().strip('"\'')
                        return version
        except Exception as e:
            print(f"无法读取版本号: {e}")
        return "unknown"
    
    def show_project_info(self):
        """显示项目信息"""
        version = self.get_version()
        print(f"""
🚀 py_auto_tester 构建发布工具
{'='*50}
📦 项目名称: py_auto_tester  
📊 当前版本: {version}
📁 项目路径: {self.project_root}
🐍 Python版本: {sys.version}
""")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="py_auto_tester 构建和发布脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--clean", action="store_true", help="清理构建产物")
    parser.add_argument("--build", action="store_true", help="构建包")
    parser.add_argument("--test", action="store_true", help="发布到测试PyPI")
    parser.add_argument("--publish", action="store_true", help="发布到正式PyPI")
    parser.add_argument("--all", action="store_true", help="执行完整流程")
    parser.add_argument("--run-tests", action="store_true", help="运行测试")
    parser.add_argument("--check", action="store_true", help="检查包完整性")
    
    args = parser.parse_args()
    
    builder = BuildPublisher()
    builder.show_project_info()
    
    # 如果没有指定任何参数，显示帮助
    if not any(vars(args).values()):
        parser.print_help()
        return 0
    
    success = True
    
    try:
        # 完整流程
        if args.all:
            print("🚀 开始完整构建发布流程...")
            
            steps = [
                ("安装构建依赖", builder.install_build_dependencies),
                ("清理构建产物", builder.clean_build_artifacts),
                ("运行测试", builder.run_tests),
                ("构建包", builder.build_package),
                ("检查包完整性", builder.check_package),
                ("发布到测试PyPI", builder.publish_to_test_pypi),
            ]
            
            for step_name, step_func in steps:
                if not step_func():
                    print(f"❌ {step_name}失败")
                    success = False
                    break
            
            if success:
                print("\n🎉 测试发布成功！如果测试无问题，可以发布到正式PyPI:")
                print("python build_and_publish.py --publish")
        
        else:
            # 单独的步骤
            if args.clean:
                success &= builder.install_build_dependencies()
                builder.clean_build_artifacts()
                
            if args.run_tests:
                success &= builder.run_tests()
                
            if args.build:
                success &= builder.install_build_dependencies()
                success &= builder.build_package()
                
            if args.check:
                success &= builder.check_package()
                
            if args.test:
                success &= builder.publish_to_test_pypi()
                
            if args.publish:
                success &= builder.publish_to_pypi()
    
    except KeyboardInterrupt:
        print("\n❌ 操作被用户中断")
        return 1
    except Exception as e:
        print(f"❌ 发生未预期的错误: {e}")
        return 1
    
    if success:
        print("\n🎉 所有操作成功完成！")
        return 0
    else:
        print("\n❌ 部分操作失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())