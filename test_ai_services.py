#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI服务测试脚本
测试OpenAI和Gemini两种AI服务是否正常工作
"""

import sys
import os
from book_classifier import BookClassifier
import config

def test_ai_service(service_name):
    """测试指定的AI服务"""
    print(f"\n测试 {service_name.upper()} 服务...")
    print("-" * 40)
    
    try:
        # 初始化分类器
        classifier = BookClassifier(ai_service=service_name)
        print(f"✓ {service_name.upper()} 分类器初始化成功")
        
        # 测试图书数据
        test_book = {
            "name": "Python深度学习实战指南",
            "abstract": "本书深入介绍Python深度学习技术，包括TensorFlow、PyTorch等框架的使用，以及神经网络、卷积神经网络、循环神经网络等核心概念。",
            "briefIntro": {
                "highlight": "Python深度学习从入门到精通，理论与实践并重",
                "authorInfo": "资深AI工程师，专注于深度学习技术研究"
            },
            "tags": [{"name": "Python"}, {"name": "深度学习"}, {"name": "AI"}],
            "categories": [[{"name": "计算机"}, {"name": "人工智能"}]]
        }
        
        # 进行分类测试
        result = classifier.classify_book(test_book)
        print(f"✓ 分类结果: {result}")
        
        return True
        
    except ImportError as e:
        print(f"✗ 导入错误: {e}")
        print("请安装必要的依赖库:")
        if service_name == 'gemini':
            print("pip install google-generativeai")
        return False
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("AI服务功能测试")
    print("=" * 60)
    
    # 检查配置
    print("检查配置...")
    print(f"默认AI服务: {config.DEFAULT_AI_SERVICE}")
    print(f"OpenAI API密钥: {'已配置' if config.OPENAI_API_KEY else '未配置'}")
    print(f"Gemini API密钥: {'已配置' if config.GEMINI_API_KEY else '未配置'}")
    
    # 测试OpenAI
    openai_success = test_ai_service('openai')
    
    # 测试Gemini
    gemini_success = test_ai_service('gemini')
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print(f"OpenAI: {'✓ 通过' if openai_success else '✗ 失败'}")
    print(f"Gemini: {'✓ 通过' if gemini_success else '✗ 失败'}")
    
    if openai_success and gemini_success:
        print("\n🎉 两种AI服务都正常工作！")
        print("你可以使用以下命令选择AI服务:")
        print("  - python main.py --ai-service openai")
        print("  - python main.py --ai-service gemini")
    elif openai_success:
        print("\n⚠️  只有OpenAI服务正常工作")
        print("Gemini服务可能需要安装依赖或检查API密钥")
    elif gemini_success:
        print("\n⚠️  只有Gemini服务正常工作")
        print("OpenAI服务可能需要检查API密钥")
    else:
        print("\n❌ 两种AI服务都无法正常工作")
        print("请检查配置和依赖安装")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 