#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图灵图书数据抓取与分析系统
主程序入口
"""

import os
import sys
import argparse
from data_scraper import IturingScraper
from book_classifier import BookClassifier
from data_analyzer import DataAnalyzer
import config

def setup_environment():
    """设置运行环境"""
    print("正在设置运行环境...")
    
    # 确保数据目录存在
    os.makedirs(config.DATA_DIR, exist_ok=True)
    os.makedirs(config.BOOKS_DIR, exist_ok=True)
    os.makedirs(config.ANALYSIS_DIR, exist_ok=True)
    
    print("环境设置完成！")

def scrape_data(max_pages=None):
    """抓取图书数据"""
    print("=" * 60)
    print("开始抓取图灵图书数据...")
    print("=" * 60)
    
    scraper = IturingScraper()
    
    # 检查是否已有数据
    existing_data = scraper.load_books_data()
    if existing_data:
        print(f"发现已有数据文件，包含 {len(existing_data)} 本图书")
        choice = input("是否重新抓取数据？(y/N): ").strip().lower()
        if choice != 'y':
            print("使用现有数据继续...")
            return existing_data
    
    # 抓取新数据
    books = scraper.scrape_all_books(max_pages=max_pages)
    
    if books:
        scraper.save_books_data(books)
        print(f"成功抓取 {len(books)} 本图书的数据")
        return books
    else:
        print("没有抓取到任何数据")
        return []

def classify_books(books, ai_service=None):
    """为图书分配技术标签"""
    print("=" * 60)
    print("开始为图书分配技术标签...")
    print("=" * 60)
    
    classifier = BookClassifier(ai_service=ai_service)
    
    # 检查是否已有分类数据
    existing_classified = classifier.load_classified_books()
    if existing_classified:
        print(f"发现已有分类数据，包含 {len(existing_classified)} 本图书")
        choice = input("是否重新分类？(y/N): ").strip().lower()
        if choice != 'y':
            print("使用现有分类数据继续...")
            return existing_classified
    
    if not books:
        print("没有图书数据可供分类")
        return []
    
    # 为图书分配技术标签
    classified_books = classifier.classify_books_batch(books)
    
    if classified_books:
        classifier.save_classified_books(classified_books)
        print(f"成功为 {len(classified_books)} 本图书分配了技术标签")
        return classified_books
    else:
        print("分类过程中出现问题")
        return []

def analyze_data():
    """分析数据并生成报告"""
    print("=" * 60)
    print("开始数据分析...")
    print("=" * 60)
    
    analyzer = DataAnalyzer()
    analyzer.run_analysis()

def run_full_pipeline(max_pages=None, ai_service=None):
    """运行完整的数据处理流程"""
    print("图灵图书数据抓取与分析系统")
    print("=" * 60)
    
    # 设置环境
    setup_environment()
    
    # 1. 抓取数据
    books = scrape_data(max_pages)
    if not books:
        print("数据抓取失败，程序退出")
        return
    
    # 2. 分类图书
    classified_books = classify_books(books, ai_service)
    if not classified_books:
        print("图书分类失败，程序退出")
        return
    
    # 3. 分析数据
    analyze_data()
    
    print("=" * 60)
    print("所有任务完成！")
    print(f"数据文件保存在: {config.BOOKS_DIR}")
    print(f"分析结果保存在: {config.ANALYSIS_DIR}")
    print("=" * 60)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='图灵图书数据抓取与分析系统')
    parser.add_argument('--max-pages', type=int, default=None, 
                       help='最大抓取页数（默认抓取所有页面）')
    parser.add_argument('--ai-service', choices=['openai', 'gemini'], 
                       default=config.DEFAULT_AI_SERVICE,
                       help=f'选择AI服务 (默认: {config.DEFAULT_AI_SERVICE})')
    parser.add_argument('--scrape-only', action='store_true',
                       help='仅抓取数据，不进行分类和分析')
    parser.add_argument('--classify-only', action='store_true',
                       help='仅进行分类，不进行数据抓取')
    parser.add_argument('--analyze-only', action='store_true',
                       help='仅进行分析，不进行数据抓取和分类')
    
    args = parser.parse_args()
    
    try:
        if args.scrape_only:
            # 仅抓取数据
            setup_environment()
            scrape_data(args.max_pages)
        elif args.classify_only:
            # 仅进行分类
            setup_environment()
            scraper = IturingScraper()
            books = scraper.load_books_data()
            if books:
                classify_books(books, args.ai_service)
            else:
                print("没有找到图书数据，请先运行数据抓取")
        elif args.analyze_only:
            # 仅进行分析
            setup_environment()
            analyze_data()
        else:
            # 运行完整流程
            run_full_pipeline(args.max_pages, args.ai_service)
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        print("详细错误信息:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 