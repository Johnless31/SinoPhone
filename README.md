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
from sinophone import chinese_to_sinophone, sinophone, chinese_to_rhymes

# 中文文本转SinoPhone编码
result = chinese_to_sinophone("中国")
print(result)  # 输出: "ZG UG"

# 拼音转SinoPhone编码
result = sinophone("zhong guo")
print(result)  # 输出: "ZG UG"

# 不使用空格连接
result = chinese_to_sinophone("中国", join_with_space=False)
print(result)  # 输出: "ZGUG"

# 提取中文文本的韵母（v0.0.3新增）
rhymes = chinese_to_rhymes("中国人民")
print(rhymes)  # 输出: ['ong', 'uo', 'en', 'in']
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

### 韵母提取示例 ✨ v0.0.3 新功能

```python
# 提取诗词韵母用于押韵分析
poem_line1 = "春眠不觉晓"
poem_line2 = "处处闻啼鸟"

rhymes1 = chinese_to_rhymes(poem_line1)
rhymes2 = chinese_to_rhymes(poem_line2)

print(f"第一句韵母: {rhymes1}")  # ['un', 'ian', 'u', 'ue', 'iao']
print(f"第二句韵母: {rhymes2}")  # ['u', 'u', 'en', 'i', 'iao']
print(f"押韵检测: {rhymes1[-1] == rhymes2[-1]}")  # True (都是'iao')
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

### `chinese_to_rhymes(chinese_text)` ✨ 新增于 v0.0.3

从中文文本中提取韵母列表。

**参数：**
- `chinese_text` (str): 中文字符串

**返回：**
- List[str]: 韵母列表

**示例：**
```python
rhymes = chinese_to_rhymes("你好世界")
print(rhymes)  # ['i', 'ao', 'i', 'ie']
```

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
- 🎵 **韵律分析**：诗词韵脚分析和押韵检测（v0.0.3新增）

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

### v0.0.3 (2025-09-10)
- ✨ **新增功能**：添加 `chinese_to_rhymes` 函数，用于提取中文文本的韵母
- 🛡️ **健壮性**：为新函数添加了完整的输入验证和错误处理
- 📝 **文档**：完善了函数文档和注释
- 🧪 **测试**：新增完备的测试用例，包含14个测试方法

### v0.0.2 (2025-09-01)
- 🎉 **初始版本发布**
- 支持中文文本和拼音文本转SinoPhone编码
- 实现语音模糊匹配规则（l/n不分、f/h不分、o/e混淆）
- 支持特殊音节处理（zhei、shei、ng、m等）
