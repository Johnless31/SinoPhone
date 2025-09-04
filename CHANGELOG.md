# 更新日志

本文档记录了 SinoPhone 项目的所有重要更改。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 计划中的功能
- 支持更多方言混淆规则
- 添加反向解码功能
- 性能优化

## [1.0.0] - 2025-01-XX

### 新增
- 初始版本发布
- 实现中文文本到SinoPhone编码的转换
- 实现拼音文本到SinoPhone编码的转换
- 支持语音模糊匹配规则：
  - l/n 不分
  - f/h 不分
  - o/e 混淆
- 支持特殊音节处理（zhei、shei、ng、m等）
- 完整的声母韵母映射表
- 支持零声母处理
- 提供灵活的输出格式（带空格或不带空格）

### 文档
- 完整的 README.md 文档
- API 使用示例
- 编码规则说明
- 应用场景介绍

### 测试
- 基本功能测试用例
- 语音混淆测试用例
- 边界情况测试

### 构建
- 标准的 Python 包结构
- setup.py 和 pyproject.toml 配置
- 支持 pip 安装
- 自动化构建脚本
