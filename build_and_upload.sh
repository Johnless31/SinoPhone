#!/bin/bash
# SinoPhone 包构建和上传脚本

set -e  # 遇到错误立即退出

echo "🚀 开始构建 SinoPhone 包..."

# 清理之前的构建文件
echo "🧹 清理旧的构建文件..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# 安装构建工具
echo "📦 安装/更新构建工具..."
python -m pip install --upgrade pip
python -m pip install --upgrade build twine

# 构建包
echo "🔨 构建源码包和wheel包..."
python -m build

# 检查构建的包
echo "🔍 检查构建的包..."
python -m twine check dist/*

echo "✅ 包构建完成！"
echo ""
echo "📋 构建的文件："
ls -la dist/
echo ""
echo "🚀 要上传到PyPI，请运行："
echo "   python -m twine upload dist/*"
echo ""
echo "🧪 要上传到TestPyPI进行测试，请运行："
echo "   python -m twine upload --repository testpypi dist/*"
echo ""
echo "💡 提示：上传前请确保已经配置了PyPI的API token"
