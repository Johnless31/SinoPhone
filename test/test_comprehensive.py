# -*- coding: utf-8 -*-
"""
SinoPhone 完备测试用例
测试覆盖：基本功能、边界值、异常情况、混淆规则、特殊音节等
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main.sinophone import (
    _sinophone_single, 
    sinophone, 
    chinese_to_sinophone,
    INITIAL_MAP,
    FINAL_MAP,
    SPECIAL_SYLLABLES
)


class TestSinophoneSingle:
    """测试 _sinophone_single 函数"""
    
    def test_basic_syllables(self):
        """测试基本音节编码"""
        # 基本声母韵母组合
        assert _sinophone_single('ba') == 'BA'
        assert _sinophone_single('pa') == 'PA'
        assert _sinophone_single('ma') == 'MA'
        assert _sinophone_single('fa') == 'HA'  # f->h 混淆
        
    def test_zero_initial_syllables(self):
        """测试零声母音节"""
        assert _sinophone_single('a') == '_A'
        assert _sinophone_single('e') == '_E'
        assert _sinophone_single('ai') == '_I'
        assert _sinophone_single('ao') == '_W'
        assert _sinophone_single('ou') == '_U'
        
    def test_complex_initials(self):
        """测试复合声母"""
        assert _sinophone_single('zhang') == 'ZG'  # zh->z, ang->g
        assert _sinophone_single('cheng') == 'CG'  # ch->c, eng->g
        assert _sinophone_single('shuang') == 'SG'  # sh->s, uang->g
        
    def test_complex_finals(self):
        """测试复合韵母"""
        assert _sinophone_single('jiang') == 'JG'  # iang->g
        assert _sinophone_single('xiong') == 'XG'  # iong->g
        assert _sinophone_single('chuang') == 'CG'  # uang->g
        
    def test_confusion_rules(self):
        """测试混淆规则"""
        # l/n 不分
        assert _sinophone_single('la') == 'NA'
        assert _sinophone_single('na') == 'NA'
        assert _sinophone_single('li') == 'NI'
        assert _sinophone_single('ni') == 'NI'
        
        # f/h 不分
        assert _sinophone_single('fa') == 'HA'
        assert _sinophone_single('ha') == 'HA'
        assert _sinophone_single('fei') == 'HV'
        assert _sinophone_single('hui') == 'HV'
        
        # 平翘舌不分
        assert _sinophone_single('za') == 'ZA'
        assert _sinophone_single('zha') == 'ZA'
        assert _sinophone_single('ca') == 'CA'
        assert _sinophone_single('cha') == 'CA'
        assert _sinophone_single('sa') == 'SA'
        assert _sinophone_single('sha') == 'SA'
        
        # o/e 混淆
        assert _sinophone_single('bo') == 'BE'
        assert _sinophone_single('be') == 'BE'
        
    def test_special_syllables(self):
        """测试特殊整体音节"""
        assert _sinophone_single('zhei') == 'ZE'
        assert _sinophone_single('shei') == 'SV'
        assert _sinophone_single('nen') == 'NN'
        assert _sinophone_single('ng') == '_E'
        assert _sinophone_single('m') == '_U'
        
    def test_edge_cases(self):
        """测试边界情况"""
        # 空字符串
        assert _sinophone_single('') == '__'
        
        # 单个字符
        assert _sinophone_single('a') == '_A'
        assert _sinophone_single('b') == 'B_'  # b作为声母，无韵母时用_
        
        # 未知音节
        assert _sinophone_single('xyz') == 'XY'  # x声母 + yz韵母(取首字母)
        
    def test_tone_handling(self):
        """测试声调处理（应该被忽略）"""
        # 这些测试假设输入已经去掉了声调
        assert _sinophone_single('zhong') == 'ZG'
        assert _sinophone_single('guo') == 'GO'  # uo->o
        
    def test_all_initials(self):
        """测试所有声母映射"""
        test_cases = [
            ('ba', 'BA'), ('pa', 'PA'), ('ma', 'MA'), ('fa', 'HA'),
            ('da', 'DA'), ('ta', 'TA'), ('na', 'NA'), ('la', 'NA'),
            ('za', 'ZA'), ('ca', 'CA'), ('sa', 'SA'),
            ('zha', 'ZA'), ('cha', 'CA'), ('sha', 'SA'), ('ra', 'RA'),
            ('ja', 'JA'), ('qa', 'QA'), ('xa', 'XA'),
            ('ga', 'GA'), ('ka', 'KA'), ('ha', 'HA'),
            ('ya', '_A'), ('wa', '_A')
        ]
        for pinyin, expected in test_cases:
            assert _sinophone_single(pinyin) == expected
            
    def test_all_finals(self):
        """测试所有韵母映射"""
        test_cases = [
            ('a', '_A'), ('ia', '_A'), ('ua', '_A'),
            ('o', '_E'), ('uo', '_O'),  # 注意：uo映射为O，单独o映射为E
            ('e', '_E'),
            ('ie', '_V'), ('ei', '_V'), ('ui', '_V'),
            ('ai', '_I'), ('uai', '_I'),
            ('ao', '_W'), ('iao', '_W'),
            ('ou', '_U'), ('iu', '_U'),
            ('an', '_N'), ('ian', '_N'), ('uan', '_N'),
            ('ang', '_G'), ('iang', '_G'), ('uang', '_G'),
            ('en', '_N'), ('in', '_N'), ('un', '_N'),
            ('eng', '_G'), ('ing', '_G'), ('ong', '_G'), ('iong', '_G'),
            ('er', '_R'),
            ('i', '_I'), ('u', '_U'), ('v', '_U')
        ]
        for pinyin, expected in test_cases:
            assert _sinophone_single(pinyin) == expected


class TestSinophone:
    """测试 sinophone 函数"""
    
    def test_single_syllable(self):
        """测试单音节"""
        assert sinophone('zhong') == 'ZG'
        assert sinophone('guo') == 'GO'
        
    def test_multiple_syllables(self):
        """测试多音节"""
        assert sinophone('zhong guo') == 'ZG GO'
        assert sinophone('zhang lao shi') == 'ZG NW SI'
        assert sinophone('li nan') == 'NI NN'
        assert sinophone('li lan') == 'NI NN'  # l/n混淆
        
    def test_confusion_pairs(self):
        """测试混淆音节对"""
        # 平翘舌 + 前后鼻音
        assert sinophone('zhong') == sinophone('zong')
        assert sinophone('zhang') == sinophone('zang')
        
        # 鼻边音
        assert sinophone('li') == sinophone('ni')
        assert sinophone('lan') == sinophone('nan')
        
        # f/h不分
        assert sinophone('fei') == sinophone('hui')
        assert sinophone('fa') == sinophone('ha')
        
    def test_empty_and_whitespace(self):
        """测试空字符串和空白字符"""
        assert sinophone('') == ''
        assert sinophone('   ') == ''  # 空格被split()处理后变成空列表
        assert sinophone('a  b') == '_A B_'
        
    def test_long_text(self):
        """测试长文本"""
        long_text = 'wo ai zhong guo wo ai bei jing'
        result = sinophone(long_text)
        expected = '_E _I ZG GO _E _I BV JG'
        assert result == expected


class TestChineseToSinophone:
    """测试 chinese_to_sinophone 函数"""
    
    def test_basic_chinese(self):
        """测试基本中文转换"""
        assert chinese_to_sinophone('中国') == 'ZG GO'
        assert chinese_to_sinophone('中国', join_with_space=False) == 'ZGGO'
        
    def test_confusion_chinese_pairs(self):
        """测试中文混淆对"""
        # l/n不分
        assert chinese_to_sinophone('李楠') == chinese_to_sinophone('李兰')
        assert chinese_to_sinophone('南') == chinese_to_sinophone('兰')
        
        # f/h不分  
        assert chinese_to_sinophone('飞') == chinese_to_sinophone('会')
        assert chinese_to_sinophone('发') == chinese_to_sinophone('哈')
        
        # 平翘舌不分
        assert chinese_to_sinophone('是') == chinese_to_sinophone('四')
        # 注意：张(zhang->ZG)和藏(cang->CG)实际上不同，因为zh->z但c保持c
        
    def test_single_character(self):
        """测试单个汉字"""
        assert chinese_to_sinophone('中') == 'ZG'
        assert chinese_to_sinophone('国') == 'GO'
        assert chinese_to_sinophone('我') == '_E'
        
    def test_long_chinese_text(self):
        """测试长中文文本"""
        text = '我爱中华人民共和国'
        result = chinese_to_sinophone(text)
        # 验证结果格式正确（包含空格分隔）
        assert len(result.split()) == len(text)
        assert all(len(code) >= 1 for code in result.split())
        
    def test_mixed_content(self):
        """测试包含非中文字符的内容"""
        # pypinyin会处理非中文字符
        result = chinese_to_sinophone('中国123')
        codes = result.split()
        assert len(codes) >= 2  # 至少包含"中"和"国"的编码
        
    def test_empty_chinese(self):
        """测试空中文字符串"""
        assert chinese_to_sinophone('') == ''
        assert chinese_to_sinophone('', join_with_space=False) == ''
        
    def test_special_chinese_characters(self):
        """测试特殊中文字符"""
        # 测试一些可能产生特殊拼音的汉字
        test_chars = ['嗯', '呣', '这', '谁']
        for char in test_chars:
            result = chinese_to_sinophone(char)
            assert isinstance(result, str)
            assert len(result) > 0


class TestMappingConsistency:
    """测试映射表一致性"""
    
    def test_initial_map_completeness(self):
        """测试声母映射表完整性"""
        # 确保所有声母都有映射
        expected_initials = [
            'b', 'p', 'm', 'f', 'd', 't', 'n', 'l',
            'z', 'c', 's', 'zh', 'ch', 'sh', 'r',
            'j', 'q', 'x', 'g', 'k', 'h', 'y', 'w'
        ]
        for initial in expected_initials:
            assert initial in INITIAL_MAP
            
    def test_final_map_completeness(self):
        """测试韵母映射表完整性"""
        # 确保常见韵母都有映射
        expected_finals = [
            'a', 'o', 'e', 'i', 'u', 'v',
            'ai', 'ei', 'ao', 'ou', 'an', 'en', 'ang', 'eng',
            'ia', 'ie', 'iao', 'iu', 'ian', 'in', 'iang', 'ing', 'iong',
            'ua', 'uo', 'uai', 'ui', 'uan', 'un', 'uang', 'ueng'
        ]
        for final in expected_finals:
            assert final in FINAL_MAP or any(final in key for key in FINAL_MAP.keys())
            
    def test_special_syllables_completeness(self):
        """测试特殊音节映射完整性"""
        for syllable in SPECIAL_SYLLABLES:
            code = SPECIAL_SYLLABLES[syllable]
            assert isinstance(code, str)
            assert len(code) >= 1


class TestPerformanceAndRobustness:
    """测试性能和健壮性"""
    
    def test_large_input(self):
        """测试大输入"""
        # 测试长拼音字符串
        long_pinyin = ' '.join(['zhang'] * 1000)
        result = sinophone(long_pinyin)
        assert len(result.split()) == 1000
        assert all(code == 'ZG' for code in result.split())
        
    def test_unicode_handling(self):
        """测试Unicode处理"""
        # 测试包含各种Unicode字符的中文
        unicode_text = '中国🇨🇳测试'
        result = chinese_to_sinophone(unicode_text)
        assert isinstance(result, str)
        
    def test_invalid_input_types(self):
        """测试无效输入类型"""
        with pytest.raises((TypeError, AttributeError)):
            sinophone(None)
        with pytest.raises((TypeError, AttributeError)):
            sinophone(123)
        with pytest.raises((TypeError, AttributeError)):
            chinese_to_sinophone(None)
        with pytest.raises((TypeError, AttributeError)):
            chinese_to_sinophone(123)


class TestRegressionCases:
    """回归测试用例"""
    
    def test_known_good_cases(self):
        """测试已知正确的用例"""
        test_cases = [
            # (输入, 预期输出)
            ('zhong guo', 'ZG GO'),
            ('zhang lao shi', 'ZG NW SI'),
            ('li nan', 'NI NN'),
            ('li lan', 'NI NN'),
            ('fei hui', 'HV HV'),
            ('shi si', 'SI SI'),
            ('yin ying', '_N _G'),
        ]
        
        for input_text, expected in test_cases:
            result = sinophone(input_text)
            assert result == expected, f"输入 '{input_text}' 期望 '{expected}' 但得到 '{result}'"
            
    def test_chinese_known_cases(self):
        """测试已知的中文用例"""
        chinese_cases = [
            ('中国', 'ZG GO'),
            ('李楠', 'NI NN'),
            ('李兰', 'NI NN'),
            ('张老师', 'ZG NW SI'),
            ('飞会', 'HV HV'),
            ('是四', 'SI SI'),
        ]
        
        for chinese, expected in chinese_cases:
            result = chinese_to_sinophone(chinese)
            assert result == expected, f"中文 '{chinese}' 期望 '{expected}' 但得到 '{result}'"


if __name__ == '__main__':
    # 可以直接运行此文件进行测试
    pytest.main([__file__, '-v'])
