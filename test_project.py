#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目功能测试脚本
"""

import os
import sys
import json
import argparse
from data_scraper import IturingScraper
from book_classifier import BookClassifier
from data_analyzer import DataAnalyzer
import config

def test_scraper():
    """测试数据抓取功能"""
    print("测试数据抓取功能...")
    
    scraper = IturingScraper()
    
    # 测试获取图书列表
    try:
        result = scraper.get_book_list(page=1)
        if result and 'bookItems' in result:
            print(f"✓ 成功获取图书列表，包含 {len(result['bookItems'])} 本图书")
            return True
        else:
            print("✗ 获取图书列表失败")
            return False
    except Exception as e:
        print(f"✗ 数据抓取测试失败: {e}")
        return False

def test_classifier(ai_service=None):
    """测试图书分类功能"""
    print(f"测试图书分类功能 (使用 {ai_service or config.DEFAULT_AI_SERVICE} API)...")
    
    try:
        classifier = BookClassifier(ai_service=ai_service)
    except Exception as e:
        print(f"✗ 分类器初始化失败: {e}")
        return False
    
    # 测试图书分类
    test_book = {
        "name": "Python深度学习实战",
        "abstract": "本书介绍Python深度学习的基础知识和实践应用，包括神经网络、卷积神经网络、循环神经网络等内容。",
        "briefIntro": {
            "highlight": "Python深度学习入门指南，理论与实践相结合",
            "authorInfo": "深度学习专家，专注于AI技术研究"
        },
        "tags": [{"name": "Python"}, {"name": "深度学习"}],
        "categories": [[{"name": "计算机"}, {"name": "人工智能"}]]
    }
    
    try:
        tag = classifier.classify_book(test_book)
        print(f"✓ 成功为测试图书分配标签: {tag}")
        return True
    except Exception as e:
        print(f"✗ 图书分类测试失败: {e}")
        return False

def test_analyzer():
    """测试数据分析功能"""
    print("测试数据分析功能...")
    
    analyzer = DataAnalyzer()
    
    # 创建测试数据
    test_books = [
        {
            "name": "Python深度学习",
            "tech_tag": "Python",
            "publishDate": "2023-01-15T00:00:00",
            "authorNameString": "张三",
            "isbn": "978-7-115-12345-6"
        },
        {
            "name": "JavaScript高级程序设计",
            "tech_tag": "JavaScript",
            "publishDate": "2023-06-20T00:00:00",
            "authorNameString": "李四",
            "isbn": "978-7-115-12346-7"
        },
        {
            "name": "机器学习实战",
            "tech_tag": "机器学习",
            "publishDate": "2022-12-10T00:00:00",
            "authorNameString": "王五",
            "isbn": "978-7-115-12347-8"
        }
    ]
    
    try:
        # 保存测试数据
        test_file = os.path.join(config.BOOKS_DIR, "test_classified_books.json")
        os.makedirs(config.BOOKS_DIR, exist_ok=True)
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_books, f, ensure_ascii=False, indent=2)
        
        # 测试数据分析
        df = analyzer.prepare_data(test_books)
        if not df.empty:
            print(f"✓ 成功处理测试数据，包含 {len(df)} 条记录")
            
            # 测试年度统计
            pivot_table = analyzer.analyze_publications_by_year(df)
            print(f"✓ 成功生成年度统计表，包含 {len(pivot_table)} 个年份")
            
            return True
        else:
            print("✗ 数据处理失败")
            return False
    except Exception as e:
        print(f"✗ 数据分析测试失败: {e}")
        return False

def test_config():
    """测试配置功能"""
    print("测试配置功能...")
    
    try:
        # 检查必要的配置项
        assert hasattr(config, 'ITURING_BASE_URL')
        assert hasattr(config, 'SEARCH_URL')
        assert hasattr(config, 'BOOK_DETAIL_URL')
        assert hasattr(config, 'REQUEST_DELAY')
        assert hasattr(config, 'TECH_CATEGORIES')
        assert hasattr(config, 'OPENAI_API_KEY')
        assert hasattr(config, 'GEMINI_API_KEY')
        assert hasattr(config, 'DEFAULT_AI_SERVICE')
        
        print("✓ 配置项检查通过")
        print(f"  - API基础URL: {config.ITURING_BASE_URL}")
        print(f"  - 请求延迟: {config.REQUEST_DELAY}秒")
        print(f"  - 技术标签数量: {len(config.TECH_CATEGORIES)}")
        print(f"  - 默认AI服务: {config.DEFAULT_AI_SERVICE}")
        print(f"  - OpenAI API密钥: {'已配置' if config.OPENAI_API_KEY else '未配置'}")
        print(f"  - Gemini API密钥: {'已配置' if config.GEMINI_API_KEY else '未配置'}")
        
        return True
    except Exception as e:
        print(f"✗ 配置测试失败: {e}")
        return False

def main():
    """运行所有测试"""
    parser = argparse.ArgumentParser(description='图灵图书数据抓取与分析系统 - 功能测试')
    parser.add_argument('--ai-service', choices=['openai', 'gemini'], 
                       default=config.DEFAULT_AI_SERVICE,
                       help=f'选择AI服务进行测试 (默认: {config.DEFAULT_AI_SERVICE})')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("图灵图书数据抓取与分析系统 - 功能测试")
    print("=" * 60)
    
    tests = [
        ("配置检查", test_config),
        ("数据抓取", test_scraper),
        ("图书分类", lambda: test_classifier(args.ai_service)),
        ("数据分析", test_analyzer)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
            else:
                print(f"  {test_name} 测试失败")
        except Exception as e:
            print(f"  {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！项目可以正常运行。")
        print("\n下一步:")
        print(f"1. 运行 'python main.py --max-pages 3 --ai-service {args.ai_service}' 进行小规模测试")
        print(f"2. 运行 'python main.py --ai-service {args.ai_service}' 进行完整数据抓取和分析")
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 