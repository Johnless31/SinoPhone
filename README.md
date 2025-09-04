# SinoPhone (中华音码)

[![PyPI version](https://badge.fury.io/py/sinophone-zh.svg)](https://badge.fury.io/py/sinophone-zh)
[![Python](https://img.shields.io/pypi/pyversions/sinophone-zh.svg)](https://pypi.org/project/sinophone-zh/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SinoPhone（中华音码）是一个用于将中文拼音转换为语音模糊哈希编码的Python库。主要用于处理中文语音识别中的同音字和方言混淆问题。

## 特性

- 🎯 **语音模糊匹配**：支持常见的方言混淆，如 l/n 不分、f/h 不分等
- 🚀 **高效编码**：将拼音音节转换为简短的哈希编码
- 🔧 **易于使用**：简单的API，支持中文文本和拼音文本输入
- 📦 **轻量级**：只依赖 pypinyin 库
- 🌏 **中文友好**：专为中文语音处理设计

## 安装

```bash
pip install sinophone-zh
```

## 快速开始

### 基本用法

```python
from sinophone import chinese_to_sinophone, sinophone

# 中文文本转SinoPhone编码
result = chinese_to_sinophone("中国")
print(result)  # 输出: "ZG UG"

# 拼音转SinoPhone编码
result = sinophone("zhong guo")
print(result)  # 输出: "ZG UG"

# 不使用空格连接
result = chinese_to_sinophone("中国", join_with_space=False)
print(result)  # 输出: "ZGUG"
```

### 语音模糊匹配示例

SinoPhone 能够处理常见的方言混淆：

```python
# l/n 不分
print(chinese_to_sinophone("南"))  # "NN"
print(chinese_to_sinophone("兰"))  # "NN" (相同编码)

# f/h 不分
print(chinese_to_sinophone("发"))  # "HI"
print(chinese_to_sinophone("花"))  # "HI" (相同编码)

# o/e 混淆
print(sinophone("bo"))  # "BE"
print(sinophone("be"))  # "BE" (相同编码)
```

## API 文档

### `chinese_to_sinophone(chinese_text, join_with_space=True)`

将中文文本转换为 SinoPhone 编码。

**参数：**
- `chinese_text` (str): 中文字符串
- `join_with_space` (bool, 可选): 是否用空格连接音节编码，默认为 True

**返回：**
- str: SinoPhone 编码字符串

### `sinophone(pinyin_text)`

将拼音文本转换为 SinoPhone 编码。

**参数：**
- `pinyin_text` (str): 拼音字符串，音节之间用空格分隔

**返回：**
- str: SinoPhone 编码字符串

## 编码规则

### 声母映射
- 标准声母：b→B, p→P, m→M, f→H, d→D, t→T, n→N, l→N 等
- 混淆规则：l/n → N, f/h → H
- 零声母：y/w/yu → _

### 韵母映射
- 标准韵母：a/ia/ua→A, o/uo→E, e→E, ai/uai→I 等
- 混淆规则：o/e → E
- 鼻音韵母：an/en系列→N, ang/eng系列→G

### 特殊音节
- zhei → ZE（"这"的口语变体）
- shei → SV（"谁"的变体）
- ng → _E（"嗯"）
- m → _U（"呣"）

## 应用场景

- 🎤 **语音识别**：处理同音字混淆
- 🔍 **模糊搜索**：中文文本的语音相似度匹配
- 📝 **输入法**：拼音输入的容错处理
- 🗣️ **方言处理**：标准普通话与方言的映射
- 🤖 **NLP应用**：中文文本的语音特征提取

## 开发

### 安装开发依赖

```bash
pip install -e .[dev]
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black .
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

## 更新日志

### v0.0.1
- 初始版本发布
- 支持中文文本和拼音文本转SinoPhone编码
- 实现语音模糊匹配规则
- 支持特殊音节处理
