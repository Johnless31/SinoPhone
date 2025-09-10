"""
SinoPhone (中华音码) - 中文拼音语音模糊哈希编码算法

这是一个用于将中文拼音转换为语音模糊哈希编码的Python库。
主要用于处理中文语音识别中的同音字和方言混淆问题。

主要功能：
- 将中文文本转换为SinoPhone编码
- 将拼音文本转换为SinoPhone编码
- 支持语音模糊匹配（如l/n不分、f/h不分等）

使用示例：
    from sinophone import chinese_to_sinophone, sinophone

    # 中文转SinoPhone编码
    result = chinese_to_sinophone("中国")
    print(result)  # 输出: "ZG UG"

    # 拼音转SinoPhone编码
    result = sinophone("zhong guo")
    print(result)  # 输出: "ZG UG"
"""

__version__ = "0.0.3"
__author__ = "johnless"
__email__ = "346656208@qq.com"
__description__ = "中华音码（SinoPhone）- 中文拼音语音模糊哈希编码算法"

from .sinophone import sinophone, chinese_to_sinophone, chinese_to_rhymes

__all__ = ["sinophone", "chinese_to_sinophone", "chinese_to_rhymes"]
