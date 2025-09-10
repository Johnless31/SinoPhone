# -*- coding: utf-8 -*-
"""
SinoPhone 安装配置文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件作为长描述
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# 读取requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    return []

setup(
    name='sinophone-zh',
    version='0.0.3',
    author='johnless', 
    author_email='346656208@qq.com', 
    description='中华音码（SinoPhone）- 中文拼音语音模糊哈希编码算法',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Johnless31/SinoPhone', 
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
    ],
    keywords='chinese pinyin phonetic hash encoding sinophone 中文 拼音 语音编码',
    python_requires='>=3.6',
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov',
            'flake8',
            'black',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/Johnless31/SinoPhone/issues',  
        'Source': 'https://github.com/Johnless31/SinoPhone',  
        'Documentation': 'https://github.com/Johnless31/SinoPhone#readme',  
    },
    include_package_data=True,
    zip_safe=False,
)
