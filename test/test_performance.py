# -*- coding: utf-8 -*-
"""
SinoPhone 性能和压力测试
测试在各种负载条件下的性能表现
"""

import pytest
import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# 添加项目根目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from main.sinophone import _sinophone_single, sinophone, chinese_to_sinophone


class TestPerformance:
    """性能测试"""
    
    def test_single_syllable_performance(self):
        """测试单音节编码性能"""
        test_syllable = 'zhang'
        iterations = 10000
        
        start_time = time.time()
        for _ in range(iterations):
            _sinophone_single(test_syllable)
        end_time = time.time()
        
        elapsed = end_time - start_time
        rate = iterations / elapsed
        
        # 期望每秒至少处理10000次
        assert rate > 10000, f"单音节编码性能过低: {rate:.2f} ops/sec"
        print(f"单音节编码性能: {rate:.2f} ops/sec")
        
    def test_multi_syllable_performance(self):
        """测试多音节编码性能"""
        test_text = 'zhong guo ren min gong he guo'
        iterations = 1000
        
        start_time = time.time()
        for _ in range(iterations):
            sinophone(test_text)
        end_time = time.time()
        
        elapsed = end_time - start_time
        rate = iterations / elapsed
        
        # 期望每秒至少处理1000次
        assert rate > 1000, f"多音节编码性能过低: {rate:.2f} ops/sec"
        print(f"多音节编码性能: {rate:.2f} ops/sec")
        
    def test_chinese_text_performance(self):
        """测试中文文本编码性能"""
        test_text = '中华人民共和国'
        iterations = 1000
        
        start_time = time.time()
        for _ in range(iterations):
            chinese_to_sinophone(test_text)
        end_time = time.time()
        
        elapsed = end_time - start_time
        rate = iterations / elapsed
        
        # 期望每秒至少处理500次（中文处理更复杂）
        assert rate > 500, f"中文编码性能过低: {rate:.2f} ops/sec"
        print(f"中文编码性能: {rate:.2f} ops/sec")


class TestScalability:
    """可扩展性测试"""
    
    def test_large_input_scaling(self):
        """测试大输入的扩展性"""
        base_text = 'zhang guo li'
        sizes = [10, 100, 1000, 5000]
        times = []
        
        for size in sizes:
            large_text = ' '.join([base_text] * size)
            
            start_time = time.time()
            result = sinophone(large_text)
            end_time = time.time()
            
            elapsed = end_time - start_time
            times.append(elapsed)
            
            # 验证结果正确性
            expected_parts = size * 3  # base_text有3个音节
            assert len(result.split()) == expected_parts
            
        # 检查时间复杂度是否接近线性
        # 理论上时间应该与输入大小成正比
        for i in range(1, len(times)):
            ratio = times[i] / times[i-1]
            size_ratio = sizes[i] / sizes[i-1]
            # 时间比率不应该显著超过大小比率（允许一些开销）
            assert ratio < size_ratio * 2, f"扩展性差: 大小比率 {size_ratio}, 时间比率 {ratio:.2f}"
            
    def test_memory_usage_scaling(self):
        """测试内存使用扩展性"""
        import psutil
        import gc
        
        process = psutil.Process()
        
        # 获取基准内存使用
        gc.collect()
        base_memory = process.memory_info().rss
        
        # 处理大量文本
        large_texts = []
        for i in range(100):
            text = f'中华人民共和国第{i}次测试'
            result = chinese_to_sinophone(text)
            large_texts.append(result)
            
        # 检查内存使用
        gc.collect()
        peak_memory = process.memory_info().rss
        memory_increase = peak_memory - base_memory
        
        # 内存增长应该是合理的（小于100MB）
        assert memory_increase < 100 * 1024 * 1024, f"内存使用过多: {memory_increase / 1024 / 1024:.2f} MB"
        print(f"内存增长: {memory_increase / 1024 / 1024:.2f} MB")


class TestConcurrency:
    """并发测试"""
    
    def test_thread_safety(self):
        """测试线程安全性"""
        test_cases = [
            'zhang guo',
            'li nan', 
            'fei hui',
            'shi si',
            'zhong guo ren min'
        ]
        
        results = {}
        errors = []
        
        def worker(case_id, text):
            try:
                result = sinophone(text)
                results[case_id] = result
            except Exception as e:
                errors.append(f"线程 {case_id}: {e}")
                
        # 创建多个线程同时处理
        threads = []
        for i, text in enumerate(test_cases * 10):  # 每个用例重复10次
            thread = threading.Thread(target=worker, args=(i, text))
            threads.append(thread)
            
        # 启动所有线程
        for thread in threads:
            thread.start()
            
        # 等待所有线程完成
        for thread in threads:
            thread.join()
            
        # 检查错误
        assert len(errors) == 0, f"线程安全性测试失败: {errors}"
        
        # 验证结果一致性
        expected_results = [sinophone(text) for text in test_cases]
        for i in range(0, len(results), len(test_cases)):
            for j, expected in enumerate(expected_results):
                actual = results.get(i + j)
                assert actual == expected, f"并发结果不一致: 期望 {expected}, 得到 {actual}"
                
    def test_concurrent_performance(self):
        """测试并发性能"""
        test_text = 'zhong guo ren min gong he guo'
        num_threads = 4
        iterations_per_thread = 250
        
        def worker():
            for _ in range(iterations_per_thread):
                sinophone(test_text)
                
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker) for _ in range(num_threads)]
            for future in futures:
                future.result()
                
        end_time = time.time()
        elapsed = end_time - start_time
        total_operations = num_threads * iterations_per_thread
        rate = total_operations / elapsed
        
        print(f"并发性能: {rate:.2f} ops/sec ({num_threads} 线程)")
        
        # 并发性能应该比单线程有所提升
        assert rate > 1000, f"并发性能过低: {rate:.2f} ops/sec"


class TestStressTest:
    """压力测试"""
    
    def test_extreme_input_sizes(self):
        """测试极端输入大小"""
        # 测试非常长的单个音节
        long_syllable = 'a' * 1000
        result = _sinophone_single(long_syllable)
        assert isinstance(result, str)
        assert len(result) >= 2
        
        # 测试大量音节
        many_syllables = ' '.join(['zhang'] * 10000)
        start_time = time.time()
        result = sinophone(many_syllables)
        end_time = time.time()
        
        assert len(result.split()) == 10000
        assert end_time - start_time < 10, "处理10000个音节耗时过长"
        
    def test_repeated_operations(self):
        """测试重复操作的稳定性"""
        test_cases = [
            'zhang',
            'zhong guo',
            '中国',
            '李楠'
        ]
        
        # 重复大量操作
        for iteration in range(1000):
            for case in test_cases:
                if any('\u4e00' <= char <= '\u9fff' for char in case):
                    result = chinese_to_sinophone(case)
                else:
                    result = sinophone(case)
                assert isinstance(result, str)
                assert len(result) > 0
                
    def test_memory_leak_detection(self):
        """测试内存泄漏"""
        import psutil
        import gc
        
        process = psutil.Process()
        
        # 记录初始内存
        gc.collect()
        initial_memory = process.memory_info().rss
        
        # 执行大量操作
        for i in range(1000):
            text = f'测试文本第{i}次迭代中华人民共和国'
            result = chinese_to_sinophone(text)
            
            # 定期检查内存
            if i % 100 == 0:
                gc.collect()
                current_memory = process.memory_info().rss
                memory_growth = current_memory - initial_memory
                
                # 内存增长应该保持在合理范围内
                max_growth = 50 * 1024 * 1024  # 50MB
                assert memory_growth < max_growth, \
                    f"可能存在内存泄漏: 增长 {memory_growth / 1024 / 1024:.2f} MB 在 {i} 次迭代后"
                    
    def test_error_resilience(self):
        """测试错误恢复能力"""
        # 混合正常和异常输入
        test_inputs = [
            'zhang',  # 正常
            '',       # 空字符串
            'xyz123', # 异常音节
            '中国',   # 正常中文
            'normal_text',  # 正常
            ' ',      # 空格
            'a' * 100,  # 超长
            '测试',   # 正常中文
        ]
        
        success_count = 0
        for input_text in test_inputs * 100:  # 重复测试
            try:
                if any('\u4e00' <= char <= '\u9fff' for char in input_text):
                    result = chinese_to_sinophone(input_text)
                else:
                    result = sinophone(input_text)
                assert isinstance(result, str)
                success_count += 1
            except Exception:
                # 某些异常输入可能会失败，但不应该影响后续操作
                pass
                
        # 大部分操作应该成功
        success_rate = success_count / (len(test_inputs) * 100)
        assert success_rate > 0.8, f"成功率过低: {success_rate:.2%}"
        print(f"错误恢复测试成功率: {success_rate:.2%}")


class TestResourceUsage:
    """资源使用测试"""
    
    def test_cpu_usage(self):
        """测试CPU使用情况"""
        import psutil
        
        # 获取当前进程
        process = psutil.Process()
        
        # 执行CPU密集型任务
        start_cpu_times = process.cpu_times()
        
        # 大量计算
        for _ in range(1000):
            text = 'zhong guo ren min gong he guo wan sui'
            sinophone(text)
            chinese_to_sinophone('中华人民共和国万岁')
            
        end_cpu_times = process.cpu_times()
        
        cpu_time_used = (end_cpu_times.user - start_cpu_times.user + 
                        end_cpu_times.system - start_cpu_times.system)
        
        print(f"CPU时间使用: {cpu_time_used:.3f} 秒")
        
        # CPU使用应该是合理的
        assert cpu_time_used < 10, f"CPU使用过多: {cpu_time_used:.3f} 秒"
        
    def test_file_handle_usage(self):
        """测试文件句柄使用"""
        import psutil
        
        process = psutil.Process()
        initial_fds = process.num_fds() if hasattr(process, 'num_fds') else 0
        
        # 执行大量操作
        for _ in range(100):
            chinese_to_sinophone('中华人民共和国')
            sinophone('zhong hua ren min gong he guo')
            
        final_fds = process.num_fds() if hasattr(process, 'num_fds') else 0
        
        # 文件句柄数量不应该增长
        if initial_fds > 0:  # 只在支持的系统上检查
            fd_growth = final_fds - initial_fds
            assert fd_growth <= 0, f"文件句柄泄漏: 增长 {fd_growth}"


if __name__ == '__main__':
    # 运行性能测试
    pytest.main([__file__, '-v', '-s'])
