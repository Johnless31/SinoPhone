# SinoPhone 发布指南

本指南将帮助您将 SinoPhone 包发布到 PyPI，让全世界的开发者都能使用您的中华音码算法。

## 📋 发布前检查清单

### 1. 更新版本信息
确保以下文件中的版本号一致：
- [ ] `main/__init__.py` 中的 `__version__`
- [ ] `setup.py` 中的 `version`
- [ ] `CHANGELOG.md` 中添加了新版本的更新说明

### 2. 更新个人信息
请在以下文件中替换占位符信息：
- [ ] `setup.py` 中的 `author` 和 `author_email`
- [ ] `setup.py` 中的 `url` 和项目链接
- [ ] `pyproject.toml` 中的作者信息和项目链接
- [ ] `main/__init__.py` 中的 `__author__` 和 `__email__`

### 3. 测试代码
- [ ] 运行所有测试：`pytest test/`
- [ ] 确保代码通过 linting：`flake8 main/`
- [ ] 手动测试主要功能

## 🚀 发布步骤

### 步骤1：注册 PyPI 账号
1. 访问 [PyPI](https://pypi.org/) 注册账号
2. 访问 [TestPyPI](https://test.pypi.org/) 注册测试账号（推荐先在测试环境发布）

### 步骤2：配置 API Token
1. 在 PyPI 账号设置中创建 API Token
2. 配置 `~/.pypirc` 文件：
```ini
[distutils]
index-servers = 
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

### 步骤3：构建包
```bash
# 使用提供的脚本
./build_and_upload.sh

# 或手动执行
python -m pip install --upgrade build twine
python -m build
```

### 步骤4：先发布到 TestPyPI（推荐）
```bash
python -m twine upload --repository testpypi dist/*
```

### 步骤5：测试安装
```bash
# 从 TestPyPI 安装测试
pip install --index-url https://test.pypi.org/simple/ sinophone-zh

# 测试功能
python -c "from sinophone import chinese_to_sinophone; print(chinese_to_sinophone('测试'))"
```

### 步骤6：发布到正式 PyPI
```bash
python -m twine upload dist/*
```

## 📦 发布后操作

### 1. 创建 Git Tag
```bash
git tag v0.0.x
git push origin v0.0.x
```

### 2. 创建 GitHub Release
1. 在 GitHub 仓库中创建新的 Release
2. 选择刚才创建的 tag
3. 添加 release notes（可以从 CHANGELOG.md 复制）

### 3. 更新文档
- [ ] 更新 README.md 中的安装说明
- [ ] 确保所有链接都指向正确的仓库地址

## 🔧 常见问题

### Q: 包名已被占用怎么办？
A: 修改 `setup.py` 和 `pyproject.toml` 中的包名，例如改为 `sinophone-zh`

### Q: 上传失败怎么办？
A: 检查：
1. API token 是否正确
2. 包名是否重复
3. 版本号是否已存在
4. 网络连接是否正常

### Q: 如何更新已发布的包？
A: 
1. 修改版本号
2. 重新构建
3. 上传新版本

### Q: 如何删除错误发布的版本？
A: PyPI 不允许删除已发布的版本，只能发布新版本进行修复

## 📞 获取帮助

- [PyPI 官方文档](https://packaging.python.org/)
- [Twine 使用指南](https://twine.readthedocs.io/)
- [Python 打包指南](https://packaging.python.org/guides/)

祝您发布顺利！🎉
