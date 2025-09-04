# -*- coding: utf-8 -*-
"""
SinoPhone 语音规则和混淆规则测试
专门测试各种语音混淆规则的正确性和完整性
"""

import pytest
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main.sinophone import _sinophone_single, sinophone, chinese_to_sinophone


class TestInitialConfusion:
    """测试声母混淆规则"""
    
    def test_ln_confusion(self):
        """测试 l/n 不分"""
        # 基本l/n混淆
        ln_pairs = [
            ('la', 'na'), ('li', 'ni'), ('lu', 'nu'), ('lv', 'nv'),
            ('lai', 'nai'), ('lei', 'nei'), ('lao', 'nao'), ('lou', 'nou'),
            ('lan', 'nan'), ('len', 'nen'), ('lang', 'nang'), ('leng', 'neng'),
            ('lia', 'nia'), ('lie', 'nie'), ('liao', 'niao'), ('liu', 'niu'),
            ('lian', 'nian'), ('lin', 'nin'), ('liang', 'niang'), ('ling', 'ning')
        ]
        
        for l_syllable, n_syllable in ln_pairs:
            l_code = _sinophone_single(l_syllable)
            n_code = _sinophone_single(n_syllable)
            assert l_code == n_code, f"l/n混淆失败: {l_syllable}({l_code}) != {n_syllable}({n_code})"
            
    def test_fh_confusion(self):
        """测试 f/h 不分"""
        fh_pairs = [
            ('fa', 'ha'), ('fo', 'ho'), ('fei', 'hei'), ('fou', 'hou'),
            ('fan', 'han'), ('fen', 'hen'), ('fang', 'hang'), ('feng', 'heng'),
            ('fu', 'hu'), ('hui', 'fui')  # 注意：fui不是标准拼音，但测试映射
        ]
        
        for f_syllable, h_syllable in fh_pairs:
            f_code = _sinophone_single(f_syllable)
            h_code = _sinophone_single(h_syllable)
            assert f_code == h_code, f"f/h混淆失败: {f_syllable}({f_code}) != {h_syllable}({h_code})"
            
    def test_flat_retroflex_confusion(self):
        """测试平翘舌不分 (z/zh, c/ch, s/sh)"""
        # z/zh 混淆
        z_zh_pairs = [
            ('za', 'zha'), ('ze', 'zhe'), ('zi', 'zhi'), ('zu', 'zhu'),
            ('zai', 'zhai'), ('zei', 'zhei'), ('zao', 'zhao'), ('zou', 'zhou'),
            ('zan', 'zhan'), ('zen', 'zhen'), ('zang', 'zhang'), ('zeng', 'zheng'),
            ('zuo', 'zhuo'), ('zui', 'zhui'), ('zuan', 'zhuan'), ('zun', 'zhun')
        ]
        
        for z_syllable, zh_syllable in z_zh_pairs:
            z_code = _sinophone_single(z_syllable)
            zh_code = _sinophone_single(zh_syllable)
            assert z_code == zh_code, f"z/zh混淆失败: {z_syllable}({z_code}) != {zh_syllable}({zh_code})"
            
        # c/ch 混淆
        c_ch_pairs = [
            ('ca', 'cha'), ('ce', 'che'), ('ci', 'chi'), ('cu', 'chu'),
            ('cai', 'chai'), ('cao', 'chao'), ('cou', 'chou'),
            ('can', 'chan'), ('cen', 'chen'), ('cang', 'chang'), ('ceng', 'cheng'),
            ('cuo', 'chuo'), ('cui', 'chui'), ('cuan', 'chuan'), ('cun', 'chun')
        ]
        
        for c_syllable, ch_syllable in c_ch_pairs:
            c_code = _sinophone_single(c_syllable)
            ch_code = _sinophone_single(ch_syllable)
            assert c_code == ch_code, f"c/ch混淆失败: {c_syllable}({c_code}) != {ch_syllable}({ch_code})"
            
        # s/sh 混淆
        s_sh_pairs = [
            ('sa', 'sha'), ('se', 'she'), ('si', 'shi'), ('su', 'shu'),
            ('sai', 'shai'), ('sao', 'shao'), ('sou', 'shou'),
            ('san', 'shan'), ('sen', 'shen'), ('sang', 'shang'), ('seng', 'sheng'),
            ('suo', 'shuo'), ('sui', 'shui'), ('suan', 'shuan'), ('sun', 'shun')
        ]
        
        for s_syllable, sh_syllable in s_sh_pairs:
            s_code = _sinophone_single(s_syllable)
            sh_code = _sinophone_single(sh_syllable)
            assert s_code == sh_code, f"s/sh混淆失败: {s_syllable}({s_code}) != {sh_syllable}({sh_code})"


class TestFinalConfusion:
    """测试韵母混淆规则"""
    
    def test_oe_confusion(self):
        """测试 o/e 混淆"""
        # 测试包含o和e的音节
        oe_pairs = [
            ('bo', 'be'), ('po', 'pe'), ('mo', 'me'), ('fo', 'fe'),
            ('do', 'de'), ('to', 'te'), ('no', 'ne'), ('lo', 'le'),
            ('go', 'ge'), ('ko', 'ke'), ('ho', 'he')
        ]
        
        for o_syllable, e_syllable in oe_pairs:
            o_code = _sinophone_single(o_syllable)
            e_code = _sinophone_single(e_syllable)
            assert o_code == e_code, f"o/e混淆失败: {o_syllable}({o_code}) != {e_syllable}({e_code})"
            
    def test_nasal_confusion(self):
        """测试鼻音混淆 (an/ang, en/eng, in/ing)"""
        # an/ang 在某些方言中可能混淆，但当前映射表中它们不同 (N vs G)
        # 这里测试映射表的一致性
        an_syllables = ['ban', 'pan', 'man', 'fan', 'dan', 'tan', 'nan', 'lan']
        ang_syllables = ['bang', 'pang', 'mang', 'fang', 'dang', 'tang', 'nang', 'lang']
        
        for syllable in an_syllables:
            code = _sinophone_single(syllable)
            assert code.endswith('N'), f"{syllable} 应该以N结尾，但得到 {code}"
            
        for syllable in ang_syllables:
            code = _sinophone_single(syllable)
            assert code.endswith('G'), f"{syllable} 应该以G结尾，但得到 {code}"
            
    def test_front_back_nasal(self):
        """测试前后鼻音 (en/eng, in/ing)"""
        # en 音节
        en_syllables = ['ben', 'pen', 'men', 'fen', 'den', 'nen', 'gen', 'hen']
        for syllable in en_syllables:
            code = _sinophone_single(syllable)
            assert code.endswith('N'), f"{syllable} 应该以N结尾，但得到 {code}"
            
        # eng 音节
        eng_syllables = ['beng', 'peng', 'meng', 'feng', 'deng', 'neng', 'geng', 'heng']
        for syllable in eng_syllables:
            code = _sinophone_single(syllable)
            assert code.endswith('G'), f"{syllable} 应该以G结尾，但得到 {code}"
            
        # in 音节
        in_syllables = ['bin', 'pin', 'min', 'din', 'tin', 'nin', 'lin']
        for syllable in in_syllables:
            code = _sinophone_single(syllable)
            assert code.endswith('N'), f"{syllable} 应该以N结尾，但得到 {code}"
            
        # ing 音节
        ing_syllables = ['bing', 'ping', 'ming', 'ding', 'ting', 'ning', 'ling']
        for syllable in ing_syllables:
            code = _sinophone_single(syllable)
            assert code.endswith('G'), f"{syllable} 应该以G结尾，但得到 {code}"


class TestToneNeutralization:
    """测试声调中性化"""
    
    def test_tone_ignored(self):
        """测试声调被忽略（假设输入已去调）"""
        # 这个测试假设输入的拼音已经去掉了声调标记
        base_syllables = ['ma', 'zhang', 'guo', 'shi', 'de']
        
        for syllable in base_syllables:
            code = _sinophone_single(syllable)
            assert isinstance(code, str)
            assert len(code) >= 2
            
    def test_same_syllable_different_tones(self):
        """测试相同音节不同声调（理论测试）"""
        # 在实际使用中，pypinyin会处理声调，这里测试基本一致性
        syllable = 'ma'
        code1 = _sinophone_single(syllable)
        code2 = _sinophone_single(syllable)
        assert code1 == code2


class TestSpecialPhoneticPhenomena:
    """测试特殊语音现象"""
    
    def test_r_coloring(self):
        """测试儿化音"""
        # 儿化音通常在韵母后加'r'
        er_syllables = ['nar', 'dianr', 'zher', 'nar']  # 假设的儿化音
        for syllable in er_syllables:
            code = _sinophone_single(syllable)
            assert isinstance(code, str)
            assert len(code) >= 2
            
    def test_neutral_tone_syllables(self):
        """测试轻声音节"""
        # 轻声音节通常是功能词
        neutral_syllables = ['de', 'le', 'ma', 'ba', 'ne']
        for syllable in neutral_syllables:
            code = _sinophone_single(syllable)
            assert isinstance(code, str)
            assert len(code) >= 2
            
    def test_syllable_boundary_issues(self):
        """测试音节边界问题"""
        # 测试可能引起音节边界歧义的情况
        ambiguous_cases = [
            'xian',  # x-ian 还是 xi-an?
            'yuan',  # yu-an 还是 y-uan?
            'liang', # li-ang 还是 l-iang?
        ]
        
        for syllable in ambiguous_cases:
            code = _sinophone_single(syllable)
            assert isinstance(code, str)
            assert len(code) == 2  # 应该产生正确的两字符编码


class TestRegionalVariations:
    """测试方言差异处理"""
    
    def test_southern_northern_differences(self):
        """测试南北方言差异"""
        # 测试一些在南北方言中发音不同的音节
        dialect_sensitive = [
            'ri',    # 日，南方可能读作 'yi'
            'zhi',   # 知，南方可能读作 'zi' 
            'chi',   # 吃，南方可能读作 'ci'
            'shi',   # 是，南方可能读作 'si'
        ]
        
        for syllable in dialect_sensitive:
            code = _sinophone_single(syllable)
            assert isinstance(code, str)
            assert len(code) >= 2
            
    def test_wu_dialect_features(self):
        """测试吴语特征（理论测试）"""
        # 吴语中可能存在的混淆
        wu_features = ['hu', 'fu', 'wu']  # 在吴语中可能混淆
        codes = [_sinophone_single(syl) for syl in wu_features]
        
        # 验证f/h混淆在编码中体现
        assert _sinophone_single('fu') == _sinophone_single('hu')
        
    def test_cantonese_influence(self):
        """测试粤语影响（理论测试）"""
        # 粤语中可能存在的特殊情况
        cantonese_influenced = ['guo', 'kuo']  # g/k在粤语中的区别
        for syllable in cantonese_influenced:
            code = _sinophone_single(syllable)
            assert isinstance(code, str)


class TestPhoneticConsistency:
    """测试语音一致性"""
    
    def test_similar_sounding_groups(self):
        """测试相似发音组"""
        # 测试应该编码相同的相似发音组
        similar_groups = [
            # l/n 组
            (['li', 'ni'], True),
            (['lan', 'nan'], True),
            (['lao', 'nao'], True),
            
            # f/h 组  
            (['fa', 'ha'], True),
            (['fei', 'hei'], True),
            (['feng', 'heng'], True),
            
            # 平翘舌组
            (['zi', 'zhi'], True),
            (['ci', 'chi'], True),
            (['si', 'shi'], True),
            
            # 不应该相同的组
            (['ba', 'pa'], False),
            (['da', 'ta'], False),
            (['ga', 'ka'], False),
        ]
        
        for syllable_group, should_be_same in similar_groups:
            codes = [_sinophone_single(syl) for syl in syllable_group]
            if should_be_same:
                assert all(code == codes[0] for code in codes), \
                    f"相似音节组 {syllable_group} 应该有相同编码，但得到 {codes}"
            else:
                assert not all(code == codes[0] for code in codes), \
                    f"不同音节组 {syllable_group} 不应该有相同编码，但都是 {codes[0]}"
                    
    def test_minimal_pairs(self):
        """测试最小对立对"""
        # 测试只有一个音素不同的音节对
        minimal_pairs = [
            ('ba', 'pa'),  # 送气与否
            ('da', 'ta'),  # 送气与否
            ('ga', 'ka'),  # 送气与否
            ('ban', 'bang'), # 前后鼻音
            ('ben', 'beng'), # 前后鼻音
            ('bin', 'bing'), # 前后鼻音
        ]
        
        for syl1, syl2 in minimal_pairs:
            code1 = _sinophone_single(syl1)
            code2 = _sinophone_single(syl2)
            # 这些应该不同（除非被混淆规则处理）
            if (syl1, syl2) not in [('ban', 'bang'), ('ben', 'beng'), ('bin', 'bing')]:
                assert code1 != code2, f"最小对立对 {syl1}/{syl2} 应该不同，但都是 {code1}"


class TestChinesePhoneticRules:
    """测试中文语音规则"""
    
    def test_chinese_confusion_pairs(self):
        """测试中文混淆对"""
        # 测试在中文环境下的混淆规则
        chinese_pairs = [
            # l/n 不分
            (('李', '尼'), True),
            (('兰', '南'), True),
            (('老', '脑'), True),
            
            # f/h 不分
            (('飞', '黑'), True),
            (('发', '哈'), True),
            (('风', '红'), True),
            
            # 平翘舌不分
            (('是', '四'), True),
            (('知', '资'), True),
            (('吃', '次'), True),
            
            # 应该不同的对
            (('巴', '怕'), False),
            (('大', '他'), False),
        ]
        
        for (char1, char2), should_be_same in chinese_pairs:
            code1 = chinese_to_sinophone(char1)
            code2 = chinese_to_sinophone(char2)
            
            if should_be_same:
                assert code1 == code2, \
                    f"中文混淆对 {char1}/{char2} 应该相同，但得到 {code1}/{code2}"
            else:
                assert code1 != code2, \
                    f"中文对比对 {char1}/{char2} 应该不同，但都是 {code1}"
                    
    def test_multi_character_consistency(self):
        """测试多字符一致性"""
        # 测试多字符词语中的混淆规则
        multi_char_cases = [
            ('李楠', '李兰'),  # l/n 混淆
            ('南京', '兰京'),  # l/n 混淆
            ('发现', '哈现'),  # f/h 混淆
            ('是的', '四的'),  # 平翘舌混淆
        ]
        
        for phrase1, phrase2 in multi_char_cases:
            code1 = chinese_to_sinophone(phrase1)
            code2 = chinese_to_sinophone(phrase2)
            assert code1 == code2, \
                f"多字符混淆 {phrase1}/{phrase2} 应该相同，但得到 {code1}/{code2}"


if __name__ == '__main__':
    # 可以直接运行此文件进行测试
    pytest.main([__file__, '-v'])
