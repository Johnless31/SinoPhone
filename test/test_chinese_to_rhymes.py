# -*- coding: utf-8 -*-
"""
chinese_to_rhymes 函数的完备测试用例
"""

import unittest
import sys
import os

# 添加父目录到路径，以便导入 sinophone 模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'main'))

from sinophone import chinese_to_rhymes


class TestChineseToRhymes(unittest.TestCase):
    """测试 chinese_to_rhymes 函数"""

    def test_basic_functionality(self):
        """测试基本功能"""
        # 基本汉字
        self.assertEqual(chinese_to_rhymes("中"), ['ong'])
        self.assertEqual(chinese_to_rhymes("国"), ['uo'])
        self.assertEqual(chinese_to_rhymes("中国"), ['ong', 'uo'])
        
        # 常见词汇
        self.assertEqual(chinese_to_rhymes("北京"), ['ei', 'ing'])
        self.assertEqual(chinese_to_rhymes("上海"), ['ang', 'ai'])
        self.assertEqual(chinese_to_rhymes("广州"), ['uang', 'ou'])

    def test_single_character(self):
        """测试单个汉字"""
        # 各种韵母类型
        self.assertEqual(chinese_to_rhymes("啊"), ['a'])      # 单韵母 a
        self.assertEqual(chinese_to_rhymes("哦"), ['o'])      # 单韵母 o
        self.assertEqual(chinese_to_rhymes("额"), ['e'])      # 单韵母 e
        self.assertEqual(chinese_to_rhymes("衣"), ['i'])      # 单韵母 i
        self.assertEqual(chinese_to_rhymes("乌"), ['u'])      # 单韵母 u
        self.assertEqual(chinese_to_rhymes("鱼"), ['v'])      # 单韵母 ü
        
        # 复韵母
        self.assertEqual(chinese_to_rhymes("爱"), ['ai'])     # ai
        self.assertEqual(chinese_to_rhymes("欧"), ['ou'])     # ou
        self.assertEqual(chinese_to_rhymes("嘿"), ['ei'])     # ei
        
        # 鼻韵母
        self.assertEqual(chinese_to_rhymes("安"), ['an'])     # an
        self.assertEqual(chinese_to_rhymes("恩"), ['en'])     # en
        self.assertEqual(chinese_to_rhymes("昂"), ['ang'])    # ang
        self.assertEqual(chinese_to_rhymes("英"), ['ing'])    # ing

    def test_multi_character_words(self):
        """测试多字词汇"""
        # 双字词
        self.assertEqual(chinese_to_rhymes("朋友"), ['eng', 'iou'])
        self.assertEqual(chinese_to_rhymes("学习"), ['ve', 'i'])
        self.assertEqual(chinese_to_rhymes("工作"), ['ong', 'uo'])
        
        # 三字词
        self.assertEqual(chinese_to_rhymes("计算机"), ['i', 'uan', 'i'])
        self.assertEqual(chinese_to_rhymes("程序员"), ['eng', 'v', 'van'])
        
        # 四字词
        self.assertEqual(chinese_to_rhymes("人工智能"), ['en', 'ong', 'i', 'eng'])
        
        # 长句子
        result = chinese_to_rhymes("我爱中华人民共和国")
        expected = ['uo', 'ai', 'ong', 'ua', 'en', 'in', 'ong', 'e', 'uo']
        self.assertEqual(result, expected)

    def test_tone_removal(self):
        """测试声调去除功能"""
        # 测试不同声调的同一个字应该返回相同的韵母
        # 注意：这里测试的是韵母提取，不是声调处理
        # 但我们需要确保声调数字被正确移除
        
        # 妈、麻、马、骂 - 都是 a 韵母
        self.assertEqual(chinese_to_rhymes("妈"), ['a'])
        self.assertEqual(chinese_to_rhymes("麻"), ['a'])
        self.assertEqual(chinese_to_rhymes("马"), ['a'])
        self.assertEqual(chinese_to_rhymes("骂"), ['a'])
        
        # 东、同、董、冻 - 都是 ong 韵母
        self.assertEqual(chinese_to_rhymes("东"), ['ong'])
        self.assertEqual(chinese_to_rhymes("同"), ['ong'])
        self.assertEqual(chinese_to_rhymes("董"), ['ong'])
        self.assertEqual(chinese_to_rhymes("冻"), ['ong'])

    def test_special_characters(self):
        """测试特殊字符和边界情况"""
        # 儿化音
        self.assertEqual(chinese_to_rhymes("花儿"), ['ua', 'er'])
        self.assertEqual(chinese_to_rhymes("这儿"), ['e', 'er'])
        
        # 轻声字
        self.assertEqual(chinese_to_rhymes("的"), ['e'])  # 轻声"的"
        self.assertEqual(chinese_to_rhymes("了"), ['e'])  # 轻声"了"
        
        # 多音字（pypinyin会选择第一个读音）
        self.assertEqual(chinese_to_rhymes("中"), ['ong'])  # 中(zhōng)
        self.assertEqual(chinese_to_rhymes("行"), ['ing'])  # 行(xíng)

    def test_punctuation_and_mixed_content(self):
        """测试标点符号和混合内容"""
        # 包含标点符号
        self.assertEqual(chinese_to_rhymes("你好！"), ['i', 'ao', '！'])
        self.assertEqual(chinese_to_rhymes("中国，加油！"), ['ong', 'uo', '，', 'ia', 'iou', '！'])
        
        # 包含数字
        self.assertEqual(chinese_to_rhymes("2023年"), ['0', 'ian'])
        
        # 包含英文字母
        self.assertEqual(chinese_to_rhymes("Hello世界"), ['Hello', 'i', 'ie'])

    def test_empty_and_whitespace(self):
        """测试空字符串和空白字符"""
        # 空字符串
        self.assertEqual(chinese_to_rhymes(""), [])
        
        # 只有空格
        self.assertEqual(chinese_to_rhymes("   "), [])
        self.assertEqual(chinese_to_rhymes(" "), [])
        
        # 包含空格的字符串
        self.assertEqual(chinese_to_rhymes("中 国"), ['ong', ' ', 'uo'])
        self.assertEqual(chinese_to_rhymes("你 好 吗"), ['i', ' ', 'ao', ' ', 'a'])

    def test_input_validation(self):
        """测试输入验证"""
        # 非字符串输入应该抛出 TypeError
        with self.assertRaises(TypeError):
            chinese_to_rhymes(None)
        
        with self.assertRaises(TypeError):
            chinese_to_rhymes(123)
        
        with self.assertRaises(TypeError):
            chinese_to_rhymes(['中', '国'])
        
        with self.assertRaises(TypeError):
            chinese_to_rhymes({'text': '中国'})

    def test_complex_syllables(self):
        """测试复杂音节"""
        # 三拼音节
        self.assertEqual(chinese_to_rhymes("庄"), ['uang'])  # zhuāng
        self.assertEqual(chinese_to_rhymes("双"), ['uang'])  # shuāng
        self.assertEqual(chinese_to_rhymes("光"), ['uang'])  # guāng
        
        # 带介音的音节
        self.assertEqual(chinese_to_rhymes("天"), ['ian'])   # tiān
        self.assertEqual(chinese_to_rhymes("年"), ['ian'])   # nián
        self.assertEqual(chinese_to_rhymes("连"), ['ian'])   # lián
        
        # ü 相关音节
        self.assertEqual(chinese_to_rhymes("女"), ['v'])     # nǚ
        self.assertEqual(chinese_to_rhymes("绿"), ['v'])     # lǜ
        self.assertEqual(chinese_to_rhymes("雪"), ['ve'])    # xuě

    def test_regional_variations(self):
        """测试可能的地方音变体"""
        # 一些可能有不同读音的字
        # 注意：pypinyin 使用标准普通话读音
        
        # 常见多音字
        self.assertEqual(chinese_to_rhymes("得"), ['e'])     # dé (得到)
        self.assertEqual(chinese_to_rhymes("和"), ['e'])     # hé (和谐)
        self.assertEqual(chinese_to_rhymes("为"), ['uei'])   # wéi (为了)

    def test_performance_large_text(self):
        """测试大文本的性能"""
        # 测试长文本
        long_text = "中华人民共和国" * 100  # 700个字符
        result = chinese_to_rhymes(long_text)
        
        # 验证结果长度
        self.assertEqual(len(result), 700)
        
        # 验证结果内容（前7个应该是重复的模式）
        expected_pattern = ['ong', 'ua', 'en', 'in', 'ong', 'e', 'uo']
        for i in range(0, 21, 7):  # 检查前3个重复周期
            self.assertEqual(result[i:i+7], expected_pattern)

    def test_edge_cases_unicode(self):
        """测试Unicode边界情况"""
        # 繁体字
        self.assertEqual(chinese_to_rhymes("國"), ['uo'])    # 繁体"国"
        self.assertEqual(chinese_to_rhymes("語"), ['v'])     # 繁体"语"
        
        # 特殊汉字
        self.assertEqual(chinese_to_rhymes("㐅"), ['u'])     # 特殊部首字符
        
        # 表情符号和汉字混合
        result = chinese_to_rhymes("你好😊世界")
        # 表情符号会被原样返回
        self.assertIn('😊', result)
        self.assertIn('i', result)   # "你"
        self.assertIn('ao', result)  # "好"

    def test_return_type_consistency(self):
        """测试返回类型一致性"""
        # 确保总是返回列表
        self.assertIsInstance(chinese_to_rhymes("中"), list)
        self.assertIsInstance(chinese_to_rhymes(""), list)
        self.assertIsInstance(chinese_to_rhymes("中国"), list)
        
        # 确保列表中的元素都是字符串
        result = chinese_to_rhymes("中华人民共和国")
        for rhyme in result:
            self.assertIsInstance(rhyme, str)

    def test_comparison_with_known_results(self):
        """测试与已知结果的对比"""
        # 一些标准测试用例
        test_cases = [
            ("春", ['uen']),
            ("夏", ['ia']),
            ("秋", ['iou']),
            ("冬", ['ong']),
            ("东南西北", ['ong', 'an', 'i', 'ei']),
            ("金木水火土", ['in', 'u', 'uei', 'uo', 'u']),
            ("一二三四五六七八九十", ['i', 'er', 'an', 'i', 'u', 'iou', 'i', 'a', 'iou', 'i']),
        ]
        
        for chinese, expected in test_cases:
            with self.subTest(chinese=chinese):
                result = chinese_to_rhymes(chinese)
                self.assertEqual(result, expected, 
                               f"字符串 '{chinese}' 期望韵母 {expected}，实际得到 {result}")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
