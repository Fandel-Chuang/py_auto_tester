#!/bin/bash
# ===================================================================
# py_auto_tester Linux/Mac 构建发布脚本
# ===================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印颜色文本
print_info() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

# 检查Python是否可用
check_python() {
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        print_error "❌ 错误: 未找到Python，请确保Python已安装"
        exit 1
    fi
    
    # 优先使用python3，如果没有则使用python
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
    
    print_success "✅ 使用Python命令: $PYTHON_CMD"
}

# 显示菜单
show_menu() {
    echo
    print_info "🚀 py_auto_tester Linux/Mac 构建发布工具"
    echo "==================================================="
    echo
    echo "请选择操作:"
    echo "1. 清理构建产物"
    echo "2. 只构建包"
    echo "3. 运行测试"
    echo "4. 构建并发布到测试PyPI"
    echo "5. 发布到正式PyPI"
    echo "6. 完整流程 (推荐)"
    echo "7. 退出"
    echo
}

# 清理构建产物
clean_build() {
    print_info "🧹 清理构建产物..."
    $PYTHON_CMD build_and_publish.py --clean
    print_success "✅ 清理完成"
}

# 构建包
build_package() {
    print_info "🔨 构建包..."
    $PYTHON_CMD build_and_publish.py --build
    print_success "✅ 构建完成"
}

# 运行测试
run_tests() {
    print_info "🧪 运行测试..."
    $PYTHON_CMD build_and_publish.py --run-tests
    print_success "✅ 测试完成"
}

# 构建并发布到测试PyPI
build_and_test() {
    print_info "🔨 构建并发布到测试PyPI..."
    $PYTHON_CMD build_and_publish.py --build --test
    echo
    print_success "📋 测试安装命令:"
    echo "pip install --index-url https://test.pypi.org/simple/ py-auto-tester"
}

# 发布到正式PyPI
publish_to_pypi() {
    print_warning "📦 发布到正式PyPI..."
    $PYTHON_CMD build_and_publish.py --publish
    echo
    print_success "📋 安装命令:"
    echo "pip install py-auto-tester"
}

# 完整流程
full_workflow() {
    print_info "🚀 执行完整构建发布流程..."
    $PYTHON_CMD build_and_publish.py --all
    echo
    print_success "📋 测试安装命令:"
    echo "pip install --index-url https://test.pypi.org/simple/ py-auto-tester"
    echo
    print_warning "如果测试无问题，运行以下命令发布到正式PyPI:"
    echo "$PYTHON_CMD build_and_publish.py --publish"
}

# 主菜单循环
main_menu() {
    while true; do
        show_menu
        read -p "请输入选项 (1-7): " choice
        
        case $choice in
            1)
                clean_build
                read -p "按回车键继续..."
                ;;
            2)
                build_package
                read -p "按回车键继续..."
                ;;
            3)
                run_tests
                read -p "按回车键继续..."
                ;;
            4)
                build_and_test
                read -p "按回车键继续..."
                ;;
            5)
                publish_to_pypi
                read -p "按回车键继续..."
                ;;
            6)
                full_workflow
                read -p "按回车键继续..."
                ;;
            7)
                print_info "👋 再见！"
                exit 0
                ;;
            *)
                print_error "❌ 无效选项，请重新选择"
                ;;
        esac
    done
}

# 主函数
main() {
    # 检查Python
    check_python
    
    # 如果有命令行参数，直接执行对应操作
    if [ $# -gt 0 ]; then
        case $1 in
            "clean")
                clean_build
                ;;
            "build")
                build_package
                ;;
            "test")
                run_tests
                ;;
            "build-test")
                build_and_test
                ;;
            "publish")
                publish_to_pypi
                ;;
            "all")
                full_workflow
                ;;
            "--help"|"-h")
                echo "用法: $0 [clean|build|test|build-test|publish|all]"
                echo "或者直接运行 $0 进入交互式菜单"
                ;;
            *)
                print_error "❌ 未知参数: $1"
                echo "用法: $0 [clean|build|test|build-test|publish|all]"
                exit 1
                ;;
        esac
    else
        # 进入交互式菜单
        main_menu
    fi
}

# 执行主函数
main "$@"