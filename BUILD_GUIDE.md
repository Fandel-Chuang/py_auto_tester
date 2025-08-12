# 构建发布脚本使用说明

## 📋 概述

本项目提供了多种构建和发布方式，适用于不同的操作系统和使用习惯：

1. **Python脚本** - 跨平台通用
2. **Windows批处理** - Windows用户友好
3. **Linux/Mac Shell脚本** - Unix系统优化
4. **Makefile** - 开发者标准工具

## 🚀 快速开始

### Windows 用户
```cmd
# 方式1: 双击运行
build_and_publish.bat

# 方式2: 命令行运行
python build_and_publish.py --all
```

### Linux/Mac 用户
```bash
# 方式1: 交互式菜单
chmod +x build_and_publish.sh
./build_and_publish.sh

# 方式2: 命令行参数
./build_and_publish.sh all

# 方式3: 使用Make
make all
```

### 通用方式（所有平台）
```bash
# Python脚本 - 推荐
python build_and_publish.py --all
```

## 📚 详细使用方法

### 1. Python脚本 (`build_and_publish.py`)

**功能最全面，跨平台兼容**

```bash
# 显示帮助
python build_and_publish.py --help

# 清理构建产物
python build_and_publish.py --clean

# 只构建包
python build_and_publish.py --build

# 运行测试
python build_and_publish.py --run-tests

# 构建并发布到测试PyPI
python build_and_publish.py --build --test

# 发布到正式PyPI
python build_and_publish.py --publish

# 完整流程（推荐）
python build_and_publish.py --all
```

### 2. Windows批处理脚本 (`build_and_publish.bat`)

**Windows用户的图形界面选择**

- 双击运行，提供交互式菜单
- 自动检查Python环境
- 彩色输出和用户友好的提示

### 3. Linux/Mac Shell脚本 (`build_and_publish.sh`)

**Unix系统的彩色交互界面**

```bash
# 赋予执行权限
chmod +x build_and_publish.sh

# 交互式运行
./build_and_publish.sh

# 直接执行特定操作
./build_and_publish.sh clean
./build_and_publish.sh build
./build_and_publish.sh all
```

### 4. Makefile (`make` 命令)

**开发者标准工具**

```bash
# 显示所有可用命令
make help

# 常用命令
make clean          # 清理
make build          # 构建
make test           # 测试
make lint           # 代码检查
make format         # 代码格式化
make test-publish   # 发布到测试PyPI
make publish        # 发布到正式PyPI
make all           # 完整开发流程
```

## 🔄 推荐工作流

### 开发阶段
```bash
# 1. 设置开发环境
make install-dev

# 2. 代码格式化
make format

# 3. 代码检查
make lint

# 4. 运行测试
make test
```

### 发布阶段
```bash
# 方式1: 使用Python脚本（推荐）
python build_and_publish.py --all

# 方式2: 使用Makefile
make all
make test-publish  # 先发布到测试PyPI测试
make publish      # 确认无误后发布到正式PyPI
```

## ⚙️ 配置文件

### `build.conf`
包含构建相关的配置参数，可以根据需要修改：
- 依赖包版本
- 路径配置
- 命令配置
- 通知设置

## 🛠️ 环境要求

### 基础要求
- Python 3.7+
- pip

### 构建依赖（自动安装）
- build
- twine  
- wheel
- setuptools

### 开发依赖（可选）
- pytest
- pytest-cov
- black
- flake8
- mypy

## 📦 发布流程

### 1. 准备阶段
```bash
# 检查当前版本
python -c "from py_auto_tester import __version__; print(__version__)"

# 更新版本号（如需要）
# 编辑以下文件中的版本号：
# - py_auto_tester/__init__.py
# - setup.py
# - pyproject.toml
# - py_auto_tester/cli.py
```

### 2. 测试阶段
```bash
# 完整测试流程
python build_and_publish.py --all
```

### 3. 发布阶段
```bash
# 发布到正式PyPI
python build_and_publish.py --publish
```

## 🔧 故障排除

### 常见问题

1. **Python命令不可用**
   - 确保Python已安装并添加到PATH
   - 尝试使用 `python3` 而不是 `python`

2. **构建失败**
   - 检查网络连接
   - 更新pip: `pip install --upgrade pip`
   - 清理后重试: `python build_and_publish.py --clean --build`

3. **发布失败**
   - 检查PyPI账户凭据
   - 确保版本号未被使用
   - 检查包名是否已存在

4. **权限问题（Linux/Mac）**
   ```bash
   chmod +x build_and_publish.sh
   ```

### 获取帮助

如果遇到问题，可以：
1. 查看详细错误信息
2. 检查网络连接
3. 更新相关依赖包
4. 提交Issue到项目仓库

## 🎯 最佳实践

1. **版本控制**: 每次发布前确保代码已提交
2. **测试优先**: 先发布到测试PyPI进行验证
3. **文档更新**: 及时更新README和CHANGELOG
4. **依赖管理**: 定期检查和更新依赖包
5. **安全检查**: 使用 `make security` 进行安全扫描

## 📈 性能优化

- 使用 `.pypirc` 文件存储PyPI凭据避免重复输入
- 配置Git钩子自动运行检查
- 使用虚拟环境隔离依赖
- 定期清理构建缓存