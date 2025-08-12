#!/usr/bin/env python
"""
修复版安装和测试脚本 - 解决权限问题
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description="", allow_fail=False):
    """运行命令并显示结果"""
    print(f"\n{'='*50}")
    if description:
        print(f"🔄 {description}")
    print(f"执行命令: {cmd}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print("✅ 输出:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ 错误:")
        print(f"退出码: {e.returncode}")
        if e.stdout:
            print("标准输出:")
            print(e.stdout)
        if e.stderr:
            print("错误输出:")
            print(e.stderr)
        
        if allow_fail:
            print("⚠️ 允许失败，继续执行...")
            return False
        else:
            return False

def main():
    print("🚀 py_auto_tester 修复版安装工具")
    print("✨ 专门解决Anaconda环境的权限问题")
    
    # 检查Python版本
    print(f"Python版本: {sys.version}")
    print(f"工作目录: {os.getcwd()}")
    
    # 卸载旧版本（使用--user）
    print("\n🗑️ 卸载旧版本...")
    run_command("pip uninstall py-auto-tester -y", "卸载旧版本", allow_fail=True)
    
    # 清理构建产物
    print("\n🧹 清理构建产物...")
    dirs_to_clean = ["build", "dist", "py_auto_tester.egg-info"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"✅ 删除: {dir_path}")
        else:
            print(f"ℹ️ 不存在: {dir_path}")
    
    # 升级构建工具（使用--user避免权限问题）
    print("\n📦 升级构建工具（使用--user选项）...")
    build_tools = ["pip", "setuptools", "wheel", "build", "twine"]
    
    for tool in build_tools:
        print(f"\n🔧 升级 {tool}...")
        if not run_command(f"pip install --user --upgrade {tool}", f"升级{tool}", allow_fail=True):
            print(f"⚠️ {tool} 升级失败，但继续...")
    
    # 构建包
    print("\n🔨 构建包...")
    if run_command("python -m build", "构建包"):
        print("✅ 构建成功")
    else:
        print("❌ 构建失败，尝试替代方法...")
        # 尝试使用setuptools直接构建
        if run_command("python setup.py sdist bdist_wheel", "使用setuptools构建"):
            print("✅ 使用setuptools构建成功")
        else:
            print("❌ 所有构建方法都失败")
            return False
    
    # 检查构建产物
    dist_path = Path("dist")
    if dist_path.exists():
        dist_files = list(dist_path.glob("*"))
        print(f"📦 构建产物: {[f.name for f in dist_files]}")
    else:
        print("❌ 未找到dist目录")
        return False
    
    # 安装包（使用--user选项）
    print("\n📦 安装包（使用--user选项）...")
    
    # 尝试安装wheel文件
    wheel_files = list(dist_path.glob("*.whl"))
    if wheel_files:
        wheel_file = wheel_files[0]
        if run_command(f"pip install --user --force-reinstall {wheel_file}", "安装wheel包"):
            print("✅ wheel包安装成功")
        else:
            print("❌ wheel包安装失败，尝试源码安装...")
            if run_command("pip install --user . --force-reinstall", "用户模式源码安装"):
                print("✅ 用户模式源码安装成功")
            else:
                print("❌ 安装失败")
                return False
    else:
        print("❌ 未找到wheel文件，尝试源码安装...")
        if run_command("pip install --user . --force-reinstall", "用户模式源码安装"):
            print("✅ 用户模式源码安装成功")
        else:
            print("❌ 安装失败")
            return False
    
    # 测试安装
    print("\n🧪 测试安装...")
    
    # 测试导入
    test_commands = [
        ("python -c \"from py_auto_tester import __version__; print(f'版本: {__version__}')\"", "测试导入和版本"),
        ("python -c \"from py_auto_tester import AutoTester; print('AutoTester导入成功')\"", "测试AutoTester导入"),
    ]
    
    # CLI测试可能因为PATH问题失败，所以单独处理
    cli_commands = [
        ("py-auto-tester --version", "测试CLI版本命令"),
        ("py-auto-tester --help", "测试CLI帮助命令"),
    ]
    
    success_count = 0
    total_tests = len(test_commands) + len(cli_commands)
    
    # 基础导入测试
    for cmd, desc in test_commands:
        if run_command(cmd, desc):
            success_count += 1
    
    # CLI测试（允许失败）
    print("\n🖥️ CLI测试（如果失败可能是PATH问题）...")
    for cmd, desc in cli_commands:
        if run_command(cmd, desc, allow_fail=True):
            success_count += 1
        else:
            print(f"⚠️ CLI命令失败，可能需要重启终端或检查PATH")
    
    print(f"\n{'='*60}")
    print(f"🎯 测试结果: {success_count}/{total_tests} 个测试通过")
    
    if success_count >= len(test_commands):  # 至少导入测试要通过
        print("🎉 核心功能安装成功！")
        
        # 显示使用方法
        print("\n📖 使用方法:")
        print("方法1 - Python模块方式:")
        print("  from py_auto_tester import AutoTester")
        print("  tester = AutoTester()")
        print("  tester.run_tests()")
        
        print("\n方法2 - 命令行方式（如果PATH正确）:")
        print("  py-auto-tester --version")
        print("  py-auto-tester --help")
        print("  py-auto-tester --from-file example_source.py")
        
        print("\n方法3 - 直接运行模块:")
        print("  python -m py_auto_tester --help")
        print("  python -m py_auto_tester --from-file example_source.py")
        
        if success_count < total_tests:
            print("\n⚠️ 注意:")
            print("- CLI命令可能需要重启终端才能使用")
            print("- 或者使用 'python -m py_auto_tester' 代替 'py-auto-tester'")
        
        return True
    else:
        print("❌ 核心功能安装失败，请检查错误信息")
        return False

if __name__ == "__main__":
    success = main()
    input("\n按回车键退出...")
    sys.exit(0 if success else 1)