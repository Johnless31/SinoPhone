# -*- coding: utf-8 -*-
"""
SinoPhone (中华音码) 算法
目标：将中文拼音转换为一个唯一的、语音模糊的哈希编码。
"""

from pypinyin import pinyin, Style, lazy_pinyin

# ====== 核心映射表 ======
# 声母映射字典
INITIAL_MAP = {
    # 标准映射
    'b': 'B', 'p': 'P', 'm': 'M',
    'd': 'D', 't': 'T',
    'z': 'Z', 'c': 'C', 's': 'S',
    'zh': 'Z', 'ch': 'C', 'sh': 'S', 'r': 'R',
    'j': 'J', 'q': 'Q', 'x': 'X',
    'g': 'G', 'k': 'K',
    'y': '_', 'w': '_', 'yu': '_',  # 零声母
    # 混淆规则映射 (覆盖标准映射)
    'l': 'N',  # 将 l 映射到 N (n的代码)，实现 l/n 不分
    'n': 'N',  # 将 n 映射到 N
    'f': 'H',  # 将 f 映射到 H (h的代码)，实现 f/h 不分
    'h': 'H',  # 将 h 映射到 H
}

# 韵母映射字典
FINAL_MAP = {
    # 标准映射
    'a': 'A', 'ia': 'A', 'ua': 'A',
    'uo': 'O',
    'ie': 'V', 'ei': 'V', 'ui': 'V', 'uei': 'V',
    'ai': 'I', 'uai': 'I',
    'ao': 'W', 'iao': 'W',
    'ou': 'U', 'iu': 'U', 'iou': 'U',
    'an': 'N', 'ian': 'N', 'uan': 'N', 'üan': 'N', 'van': 'N',
    'ang': 'G', 'iang': 'G', 'uang': 'G',
    'en': 'N', 'in': 'N', 'un': 'N', 'ün': 'N', 'ven': 'N',
    'eng': 'G', 'ing': 'G', 'ueng': 'G', 'ong': 'G', 'iong': 'G',
    'er': 'R',
    'i': 'I', 'u': 'U', 'v': 'U', 'ü': 'U',
    # 混淆规则映射 (o和e都映射到E)
    'o': 'E',  # o -> e 混淆
    'e': 'E',  # e -> o 混淆
}

# 特殊整体音节映射（优先级最高）
SPECIAL_SYLLABLES = {
    'zhei': 'ZE',  # "这" zhe 的口语变体
    'zei': 'ZE',   # 为了与zhei混淆，zei也映射到ZE
    'shei': 'SV',  # "谁" shui 的变体
    'nen': 'NN',   # "您" nin 的变体
    'ng': '_E',    # "嗯" ng
    'm': '_U',     # "呣" m
}


def _sinophone_single(pinyin_syllable):
    """
    对单个拼音音节进行 SinoPhone 编码。
    :param pinyin_syllable: 单个音节字符串，如 "zhang", "ai"
    :return: 编码字符串，如 "ZG"
    """
    # 输入验证和预处理
    if not isinstance(pinyin_syllable, str):
        raise TypeError(f"输入必须是字符串，得到 {type(pinyin_syllable)}")

    # 转换为小写并去除空白字符
    pinyin_syllable = pinyin_syllable.lower().strip()

    # 处理空字符串
    if not pinyin_syllable:
        return '__'

    # 0. 检查特殊整体音节
    if pinyin_syllable in SPECIAL_SYLLABLES:
        return SPECIAL_SYLLABLES[pinyin_syllable]

    # 1. 分离声母和韵母（简化处理）
    initial_part = ''
    final_part = pinyin_syllable

    # 检查常见的声母组合（从长到短）
    possible_initials = ['zh', 'ch', 'sh', 'b', 'p', 'm', 'f', 'd', 't',
                         'n', 'l', 'z', 'c', 's', 'j', 'q', 'x', 'g',
                         'k', 'h', 'r', 'y', 'w']
    for possible_initial in possible_initials:
        if pinyin_syllable.startswith(possible_initial):
            initial_part = possible_initial
            final_part = pinyin_syllable[len(initial_part):]  # 剩余部分作为韵母
            break
    # 如果没有匹配到声母，则整个音节视为韵母（零声母）
    if not initial_part:
        initial_part = ''  # 零声母
        final_part = pinyin_syllable

    # 2. 映射声母
    initial_code = INITIAL_MAP.get(initial_part, '_')  # 默认用_表示零声母或未知

    # 3. 映射韵母
    # 优先尝试匹配最长的可能韵母
    final_code = '?'
    # 按长度降序排序的韵母键，确保优先匹配长的（如'iang'先于'ang'）
    sorted_final_keys = sorted(FINAL_MAP.keys(), key=len, reverse=True)
    for possible_final in sorted_final_keys:
        if final_part == possible_final:
            final_code = FINAL_MAP[possible_final]
            break
    else:
        # 如果没有完全匹配，尝试简单匹配（后备策略）
        if final_part:
            final_code = final_part[0].upper()  # 取第一个字符的大写
        else:
            final_code = '_'

    # 4. 组合代码
    return initial_code + final_code


def sinophone(pinyin_text):
    """
    对完整的拼音字符串（可能包含多个音节）进行 SinoPhone 编码。
    默认处理方式：将每个音节的SinoPhone码用空格连接。
    :param pinyin_text: 拼音字符串，如 "zhong guo"
    :return: 编码字符串，如 "ZG GO"
    """
    # 输入验证
    if not isinstance(pinyin_text, str):
        raise TypeError(f"输入必须是字符串，得到 {type(pinyin_text)}")

    # 处理空字符串
    if not pinyin_text.strip():
        return ''

    # 分割音节，过滤空字符串
    syllables = [syl for syl in pinyin_text.split() if syl.strip()]

    # 如果没有有效音节，返回空字符串
    if not syllables:
        return ''

    coded_syllables = [_sinophone_single(syl) for syl in syllables]
    return ' '.join(coded_syllables)


def chinese_to_sinophone(chinese_text, join_with_space=True):
    """
    将中文短语转换为 SinoPhone 音码。
    :param chinese_text: 中文字符串，如 "中国"
    :param join_with_space: 是否用空格连接音节码，默认True
    :return: 编码字符串，如 "ZG GO" 或 "ZGGO"
    """
    # 输入验证
    if not isinstance(chinese_text, str):
        raise TypeError(f"输入必须是字符串，得到 {type(chinese_text)}")

    # 处理空字符串
    if not chinese_text.strip():
        return ''

    # 使用pypinyin获取拼音，不带声调
    pinyin_list = pinyin(chinese_text, style=Style.NORMAL)

    # 将拼音转换为SinoPhone码
    coded_syllables = []
    for syllable_list in pinyin_list:
        # 每个syllable_list包含一个拼音音节
        syllable = syllable_list[0]  # 取第一个（通常只有一个）
        if syllable.strip():  # 只处理非空音节
            coded_syllables.append(_sinophone_single(syllable))

    # 如果没有有效音节，返回空字符串
    if not coded_syllables:
        return ''

    if join_with_space:
        return ' '.join(coded_syllables)
    else:
        return ''.join(coded_syllables)

def chinese_to_rhymes(chinese_text):
    """
    将中文短语转换为韵母列表。
    :param chinese_text: 中文字符串，如 "中国"
    :return: 韵母列表，如 ['ong', 'uo']
    """
    # 输入验证
    if not isinstance(chinese_text, str):
        raise TypeError(f"输入必须是字符串，得到 {type(chinese_text)}")

    # 处理空字符串
    if not chinese_text.strip():
        return []

    # 使用 lazy_pinyin 函数获取每个字的拼音，并指定 Style.FINALS_TONE2 来获取韵母和声调
    pinyins_with_tones = lazy_pinyin(chinese_text, style=Style.FINALS_TONE2)
    
    rhymes = []
    for pinyin in pinyins_with_tones:
        # 移除韵母中的数字声调（声调可能在中间位置）
        rhyme = ''.join(char for char in pinyin if char not in '1234')
        rhymes.append(rhyme)
    
    return rhymes