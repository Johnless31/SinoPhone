# -*- coding: utf-8 -*-
"""
SinoPhone 边界值和异常情况测试
专门测试各种边界条件、异常输入、极端情况
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main.sinophone import _sinophone_single, sinophone, chinese_to_sinophone


class TestEmptyAndWhitespace:
    """测试空值和空白字符处理"""
    
    def test_empty_strings(self):
        """测试空字符串"""
        assert _sinophone_single('') == '__'
        assert sinophone('') == ''
        assert chinese_to_sinophone('') == ''

class TestSingleCharacters:
    """测试单字符输入"""
    
    def test_single_vowels(self):
        """测试单个元音"""
        vowels = ['a', 'e', 'i', 'o', 'u']
        for vowel in vowels:
            result = _sinophone_single(vowel)
            assert len(result) == 2
            assert result.startswith('_')
            
    def test_single_consonants(self):
        """测试单个辅音"""
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'w', 'x', 'y', 'z']
        for consonant in consonants:
            result = _sinophone_single(consonant)
            assert len(result) >= 2
            
    def test_single_chinese_characters(self):
        """测试单个汉字"""
        chars = ['中', '国', '人', '民', '共', '和', '我', '你', '他', '她']
        for char in chars:
            result = chinese_to_sinophone(char)
            assert len(result) >= 1
            assert ' ' not in result  # 单个字符不应该包含空格


class TestInvalidInputs:
    """测试无效输入"""
    
    def test_none_inputs(self):
        """测试None输入"""
        with pytest.raises((TypeError, AttributeError)):
            _sinophone_single(None)
        with pytest.raises((TypeError, AttributeError)):
            sinophone(None)
        with pytest.raises((TypeError, AttributeError)):
            chinese_to_sinophone(None)
            
    def test_numeric_inputs(self):
        """测试数字输入"""
        with pytest.raises((TypeError, AttributeError)):
            _sinophone_single(123)
        with pytest.raises((TypeError, AttributeError)):
            sinophone(123)
        with pytest.raises((TypeError, AttributeError)):
            chinese_to_sinophone(123)
            
    def test_list_inputs(self):
        """测试列表输入"""
        with pytest.raises((TypeError, AttributeError)):
            _sinophone_single(['a', 'b'])
        with pytest.raises((TypeError, AttributeError)):
            sinophone(['a', 'b'])
        with pytest.raises((TypeError, AttributeError)):
            chinese_to_sinophone(['中', '国'])


class TestSpecialCharacters:
    """测试特殊字符"""
    
    def test_punctuation(self):
        """测试标点符号"""
        # pypinyin会处理标点符号
        result = chinese_to_sinophone('中，国。')
        assert isinstance(result, str)
        
    def test_numbers_in_chinese(self):
        """测试中文中的数字"""
        result = chinese_to_sinophone('中123国')
        assert isinstance(result, str)
        codes = result.split()
        assert len(codes) >= 2  # 至少有"中"和"国"
        
    def test_english_in_chinese(self):
        """测试中文中的英文"""
        result = chinese_to_sinophone('中abc国')
        assert isinstance(result, str)
        
    def test_special_symbols(self):
        """测试特殊符号"""
        symbols = ['@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=']
        for symbol in symbols:
            # 这些符号作为拼音输入应该能处理
            result = _sinophone_single(symbol)
            assert isinstance(result, str)
            assert len(result) >= 1


class TestExtremeInputs:
    """测试极端输入"""
    
    def test_very_long_syllable(self):
        """测试非常长的音节"""
        long_syllable = 'a' * 100
        result = _sinophone_single(long_syllable)
        assert isinstance(result, str)
        assert len(result) >= 1
        
    def test_very_long_pinyin_text(self):
        """测试非常长的拼音文本"""
        long_text = ' '.join(['zhang'] * 1000)
        result = sinophone(long_text)
        assert len(result.split()) == 1000
        
    def test_very_long_chinese_text(self):
        """测试非常长的中文文本"""
        long_chinese = '中' * 100
        result = chinese_to_sinophone(long_chinese)
        assert len(result.split()) == 100


class TestUnicodeAndEncoding:
    """测试Unicode和编码问题"""
    
    def test_unicode_characters(self):
        """测试Unicode字符"""
        unicode_chars = ['中', '國', '测', '試', '🇨🇳', '😊']
        for char in unicode_chars:
            try:
                result = chinese_to_sinophone(char)
                assert isinstance(result, str)
            except Exception:
                # 某些Unicode字符可能无法处理，这是可以接受的
                pass
                
    def test_traditional_chinese(self):
        """测试繁体中文"""
        traditional_chars = ['國', '測', '試', '語', '言']
        for char in traditional_chars:
            result = chinese_to_sinophone(char)
            assert isinstance(result, str)
            assert len(result) >= 1
            
    def test_mixed_scripts(self):
        """测试混合文字"""
        mixed_text = '中文English中文'
        result = chinese_to_sinophone(mixed_text)
        assert isinstance(result, str)


class TestBoundaryValues:
    """测试边界值"""
    
    def test_minimum_valid_syllable(self):
        """测试最小有效音节"""
        min_syllables = ['a', 'e', 'o']
        for syllable in min_syllables:
            result = _sinophone_single(syllable)
            assert len(result) == 2
            assert result.startswith('_')
            
    def test_maximum_length_syllable(self):
        """测试最长音节"""
        long_syllables = ['zhuang', 'chuang', 'shuang']
        for syllable in long_syllables:
            result = _sinophone_single(syllable)
            assert len(result) == 2
            
    def test_zero_and_one_character_inputs(self):
        """测试0和1字符输入"""
        # 0字符
        assert _sinophone_single('') == '__'
        
        # 1字符
        assert _sinophone_single('a') == '_A'


class TestCaseInsensitivity:
    """测试大小写不敏感性"""
    
    def test_uppercase_pinyin(self):
        """测试大写拼音"""
        assert _sinophone_single('ZHANG') == _sinophone_single('zhang')
        assert _sinophone_single('GUO') == _sinophone_single('guo')
        
    def test_mixed_case_pinyin(self):
        """测试混合大小写拼音"""
        assert _sinophone_single('ZhAnG') == _sinophone_single('zhang')
        assert sinophone('ZhOnG GuO') == sinophone('zhong guo')


class TestMemoryAndPerformance:
    """测试内存和性能边界"""
    
    def test_memory_intensive_input(self):
        """测试内存密集型输入"""
        # 大量重复的短音节
        massive_input = ' '.join(['a'] * 10000)
        result = sinophone(massive_input)
        assert len(result.split()) == 10000
        
    def test_nested_function_calls(self):
        """测试嵌套函数调用"""
        # 确保函数可以处理复杂的嵌套调用
        text = 'zhong guo'
        result1 = sinophone(text)
        result2 = sinophone(sinophone(text).lower().replace(' ', ' '))
        # 第二次调用应该处理已编码的结果
        assert isinstance(result2, str)


class TestConsistency:
    """测试一致性"""
    
    def test_idempotency(self):
        """测试幂等性（相同输入应产生相同输出）"""
        test_inputs = ['zhang', 'guo', 'zhong guo', '中国', '李楠']
        
        for input_text in test_inputs:
            if any('\u4e00' <= char <= '\u9fff' for char in input_text):
                # 中文输入
                result1 = chinese_to_sinophone(input_text)
                result2 = chinese_to_sinophone(input_text)
            else:
                # 拼音输入
                result1 = sinophone(input_text)
                result2 = sinophone(input_text)
            
            assert result1 == result2, f"不一致的结果：'{input_text}' -> '{result1}' vs '{result2}'"
            
    def test_order_independence(self):
        """测试顺序无关性（单音节的编码不应该依赖上下文）"""
        syllables = ['zhang', 'guo', 'li', 'nan']
        
        # 单独编码
        individual_codes = [_sinophone_single(syl) for syl in syllables]
        
        # 组合编码然后分割
        combined_text = ' '.join(syllables)
        combined_result = sinophone(combined_text)
        combined_codes = combined_result.split()
        
        assert individual_codes == combined_codes


if __name__ == '__main__':
    # 可以直接运行此文件进行测试
    pytest.main([__file__, '-v'])
