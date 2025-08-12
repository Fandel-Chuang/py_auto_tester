@echo off
REM ===================================================================
REM py_auto_tester Windows 构建发布脚本
REM ===================================================================

echo 🚀 py_auto_tester Windows 构建发布工具
echo ===================================================

REM 检查Python是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

REM 显示菜单
:menu
echo.
echo 请选择操作:
echo 1. 清理构建产物
echo 2. 只构建包
echo 3. 运行测试
echo 4. 构建并发布到测试PyPI
echo 5. 发布到正式PyPI
echo 6. 完整流程 (推荐)
echo 7. 退出
echo.

set /p choice="请输入选项 (1-7): "

if "%choice%"=="1" goto clean
if "%choice%"=="2" goto build
if "%choice%"=="3" goto test
if "%choice%"=="4" goto build_test
if "%choice%"=="5" goto publish
if "%choice%"=="6" goto all
if "%choice%"=="7" goto exit
echo ❌ 无效选项，请重新选择
goto menu

:clean
echo 🧹 清理构建产物...
python build_and_publish.py --clean
if %errorlevel% neq 0 echo ❌ 清理失败
pause
goto menu

:build
echo 🔨 构建包...
python build_and_publish.py --build
if %errorlevel% neq 0 echo ❌ 构建失败
pause
goto menu

:test
echo 🧪 运行测试...
python build_and_publish.py --run-tests
if %errorlevel% neq 0 echo ❌ 测试失败
pause
goto menu

:build_test
echo 🔨 构建并发布到测试PyPI...
python build_and_publish.py --build --test
if %errorlevel% neq 0 echo ❌ 操作失败
echo.
echo 📋 测试安装命令:
echo pip install --index-url https://test.pypi.org/simple/ py-auto-tester
pause
goto menu

:publish
echo 📦 发布到正式PyPI...
python build_and_publish.py --publish
if %errorlevel% neq 0 echo ❌ 发布失败
echo.
echo 📋 安装命令:
echo pip install py-auto-tester
pause
goto menu

:all
echo 🚀 执行完整构建发布流程...
python build_and_publish.py --all
if %errorlevel% neq 0 (
    echo ❌ 流程失败
) else (
    echo ✅ 流程成功完成
    echo.
    echo 📋 测试安装命令:
    echo pip install --index-url https://test.pypi.org/simple/ py-auto-tester
    echo.
    echo 如果测试无问题，运行以下命令发布到正式PyPI:
    echo python build_and_publish.py --publish
)
pause
goto menu

:exit
echo 👋 再见！
exit /b 0