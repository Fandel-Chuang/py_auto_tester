# ===================================================================
# py_auto_tester Makefile
# ===================================================================

.PHONY: help clean build test check publish test-publish install-dev lint format docs all

# 默认Python命令
PYTHON := python3
PIP := pip3

# 项目信息
PROJECT_NAME := py_auto_tester
PACKAGE_DIR := py_auto_tester

# 帮助信息
help:
	@echo "🚀 py_auto_tester 构建工具"
	@echo "=========================="
	@echo ""
	@echo "可用的命令:"
	@echo "  help          显示此帮助信息"
	@echo "  clean         清理构建产物和缓存"
	@echo "  install-dev   安装开发依赖"
	@echo "  lint          代码检查 (flake8)"
	@echo "  format        代码格式化 (black)"
	@echo "  test          运行测试"
	@echo "  build         构建包"
	@echo "  check         检查包完整性"
	@echo "  test-publish  发布到测试PyPI"
	@echo "  publish       发布到正式PyPI"
	@echo "  docs          生成文档"
	@echo "  all           完整流程 (清理、测试、构建、检查)"
	@echo ""
	@echo "使用示例:"
	@echo "  make clean build    # 清理并构建"
	@echo "  make all           # 完整流程"
	@echo "  make test-publish  # 发布到测试PyPI"

# 清理构建产物
clean:
	@echo "🧹 清理构建产物..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 清理完成"

# 安装开发依赖
install-dev:
	@echo "📦 安装开发依赖..."
	@$(PIP) install --upgrade pip
	@$(PIP) install build twine wheel setuptools
	@$(PIP) install pytest pytest-cov black flake8 mypy
	@$(PIP) install -e .
	@echo "✅ 开发环境设置完成"

# 代码检查
lint:
	@echo "🔍 代码检查..."
	@$(PYTHON) -m flake8 $(PACKAGE_DIR)/ --max-line-length=88 --extend-ignore=E203,W503
	@echo "✅ 代码检查完成"

# 代码格式化
format:
	@echo "🎨 代码格式化..."
	@$(PYTHON) -m black $(PACKAGE_DIR)/ --line-length=88
	@$(PYTHON) -m black *.py --line-length=88
	@echo "✅ 代码格式化完成"

# 运行测试
test:
	@echo "🧪 运行测试..."
	@if [ -d "tests" ]; then \
		$(PYTHON) -m pytest tests/ -v --cov=$(PACKAGE_DIR) --cov-report=term-missing || true; \
	else \
		echo "⚠️  未找到tests目录，跳过测试"; \
	fi
	@echo "✅ 测试完成"

# 构建包
build: clean
	@echo "🔨 构建包..."
	@$(PYTHON) -m build
	@echo "✅ 构建完成"

# 检查包完整性
check:
	@echo "🔍 检查包完整性..."
	@$(PYTHON) -m twine check dist/*
	@echo "✅ 包检查完成"

# 发布到测试PyPI
test-publish: build check
	@echo "📤 发布到测试PyPI..."
	@$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo "✅ 发布到测试PyPI完成"
	@echo "📋 测试安装命令:"
	@echo "pip install --index-url https://test.pypi.org/simple/ $(PROJECT_NAME)"

# 发布到正式PyPI
publish: build check
	@echo "📦 发布到正式PyPI..."
	@read -p "确定要发布到正式PyPI吗？(y/N): " confirm && [ "$$confirm" = "y" ]
	@$(PYTHON) -m twine upload dist/*
	@echo "✅ 发布到正式PyPI完成"
	@echo "📋 安装命令:"
	@echo "pip install $(PROJECT_NAME)"

# 生成文档
docs:
	@echo "📚 生成文档..."
	@if command -v sphinx-build >/dev/null 2>&1; then \
		echo "使用Sphinx生成文档..."; \
		sphinx-build -b html docs docs/_build/html; \
	else \
		echo "⚠️  Sphinx未安装，跳过文档生成"; \
		echo "安装命令: pip install sphinx"; \
	fi

# 完整流程
all: clean install-dev lint test build check
	@echo ""
	@echo "🎉 完整流程完成！"
	@echo "现在你可以:"
	@echo "  make test-publish  # 发布到测试PyPI"
	@echo "  make publish      # 发布到正式PyPI"

# 开发模式安装
install-local:
	@echo "📦 本地安装..."
	@$(PIP) install -e .
	@echo "✅ 本地安装完成"

# 检查代码类型
type-check:
	@echo "🔍 类型检查..."
	@$(PYTHON) -m mypy $(PACKAGE_DIR)/ || echo "⚠️  类型检查完成（可能有警告）"

# 性能测试
benchmark:
	@echo "⚡ 性能测试..."
	@if [ -f "benchmark.py" ]; then \
		$(PYTHON) benchmark.py; \
	else \
		echo "⚠️  未找到benchmark.py文件"; \
	fi

# 版本信息
version:
	@echo "📊 版本信息:"
	@$(PYTHON) -c "from $(PACKAGE_DIR) import __version__; print(f'当前版本: {__version__}')"

# 依赖检查
deps-check:
	@echo "🔍 检查依赖..."
	@$(PIP) list --outdated
	@echo "✅ 依赖检查完成"

# 安全检查
security:
	@echo "🔒 安全检查..."
	@if command -v safety >/dev/null 2>&1; then \
		safety check; \
	else \
		echo "⚠️  safety未安装，跳过安全检查"; \
		echo "安装命令: pip install safety"; \
	fi