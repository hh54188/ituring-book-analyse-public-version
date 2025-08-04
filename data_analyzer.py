import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from typing import List, Dict, Any
from datetime import datetime
import config

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class DataAnalyzer:
    def __init__(self):
        self.books_data = []
        
    def load_classified_books(self, filename: str = "classified_books.json") -> List[Dict[str, Any]]:
        """加载已分类的图书数据"""
        filepath = os.path.join(config.BOOKS_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"分类数据文件不存在: {filepath}")
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def parse_publish_date(self, date_str: str) -> int:
        """解析出版日期，返回年份"""
        try:
            if date_str:
                # 处理不同的日期格式
                if 'T' in date_str:
                    date_str = date_str.split('T')[0]
                
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                return date_obj.year
            return None
        except:
            return None
    
    def prepare_data(self, books: List[Dict[str, Any]]) -> pd.DataFrame:
        """准备分析数据"""
        data = []
        
        for book in books:
            # 提取关键信息
            name = book.get('name', '')
            tech_tag = book.get('tech_tag', '其他')
            publish_date = book.get('publishDate', '')
            author = book.get('authorNameString', '')
            isbn = book.get('isbn', '')
            
            # 跳过"其他"标签的图书
            if tech_tag == '其他':
                continue
            
            # 解析出版年份
            year = self.parse_publish_date(publish_date)
            
            if year:
                data.append({
                    'name': name,
                    'tech_tag': tech_tag,
                    'publish_year': year,
                    'author': author,
                    'isbn': isbn,
                    'publish_date': publish_date
                })
        
        return pd.DataFrame(data)
    
    def analyze_publications_by_year(self, df: pd.DataFrame) -> pd.DataFrame:
        """分析每年各技术标签的出版数量"""
        # 按年份和技术标签分组统计
        yearly_stats = df.groupby(['publish_year', 'tech_tag']).size().reset_index(name='count')
        
        # 透视表，行为年份，列为技术标签
        pivot_table = yearly_stats.pivot(index='publish_year', columns='tech_tag', values='count').fillna(0)
        
        return pivot_table
    
    def create_visualizations(self, df: pd.DataFrame, pivot_table: pd.DataFrame):
        """创建可视化图表"""
        # 确保分析目录存在
        os.makedirs(config.ANALYSIS_DIR, exist_ok=True)
        
        # 1. 总体技术标签分布饼图
        plt.figure(figsize=(12, 8))
        tech_counts = df['tech_tag'].value_counts()
        plt.pie(tech_counts.values, labels=tech_counts.index, autopct='%1.1f%%')
        plt.title('图灵图书技术标签分布', fontsize=16, fontweight='bold')
        plt.axis('equal')
        plt.savefig(os.path.join(config.ANALYSIS_DIR, 'tech_tag_distribution.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. 每年各技术标签出版数量堆叠柱状图
        plt.figure(figsize=(16, 10))
        
        # 选择出版数量最多的前10个技术标签
        top_tags = df['tech_tag'].value_counts().head(10).index
        
        # 筛选数据
        filtered_df = df[df['tech_tag'].isin(top_tags)]
        filtered_pivot = filtered_df.groupby(['publish_year', 'tech_tag']).size().reset_index(name='count')
        
        # 创建堆叠柱状图
        pivot_for_plot = filtered_pivot.pivot(index='publish_year', columns='tech_tag', values='count').fillna(0)
        
        ax = pivot_for_plot.plot(kind='bar', stacked=True, figsize=(16, 10))
        plt.title('图灵图书各技术标签年度出版数量趋势', fontsize=16, fontweight='bold')
        plt.xlabel('出版年份', fontsize=12)
        plt.ylabel('图书数量', fontsize=12)
        plt.legend(title='技术标签', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(config.ANALYSIS_DIR, 'yearly_tech_tag_trend.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. 热力图
        plt.figure(figsize=(14, 10))
        sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': '图书数量'})
        plt.title('图灵图书技术标签年度出版热力图', fontsize=16, fontweight='bold')
        plt.xlabel('技术标签', fontsize=12)
        plt.ylabel('出版年份', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(config.ANALYSIS_DIR, 'tech_tag_year_heatmap.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 4. 年度出版总量趋势
        plt.figure(figsize=(12, 8))
        yearly_total = df.groupby('publish_year').size()
        plt.plot(yearly_total.index, yearly_total.values, marker='o', linewidth=2, markersize=8)
        plt.title('图灵图书年度出版总量趋势', fontsize=16, fontweight='bold')
        plt.xlabel('出版年份', fontsize=12)
        plt.ylabel('图书数量', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(config.ANALYSIS_DIR, 'yearly_total_publications.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_statistics_report(self, df: pd.DataFrame, pivot_table: pd.DataFrame) -> str:
        """生成统计报告"""
        report = []
        report.append("=" * 60)
        report.append("图灵图书数据分析报告")
        report.append("=" * 60)
        report.append("")
        
        # 基本统计信息
        report.append("1. 基本统计信息")
        report.append("-" * 30)
        report.append(f"总图书数量: {len(df)}")
        report.append(f"数据年份范围: {df['publish_year'].min()} - {df['publish_year'].max()}")
        report.append(f"技术标签数量: {df['tech_tag'].nunique()}")
        report.append("")
        
        # 技术标签分布
        report.append("2. 技术标签分布 (前10名)")
        report.append("-" * 30)
        tech_counts = df['tech_tag'].value_counts()
        for i, (tag, count) in enumerate(tech_counts.head(10).items(), 1):
            percentage = (count / len(df)) * 100
            report.append(f"{i:2d}. {tag:<15} {count:4d} 本 ({percentage:5.1f}%)")
        report.append("")
        
        # 年度趋势
        report.append("3. 年度出版趋势")
        report.append("-" * 30)
        yearly_total = df.groupby('publish_year').size()
        for year, count in yearly_total.items():
            report.append(f"{year}: {count} 本")
        report.append("")
        
        # 最活跃的技术标签年度
        report.append("4. 各技术标签最活跃年份")
        report.append("-" * 30)
        for tag in tech_counts.head(10).index:
            tag_data = df[df['tech_tag'] == tag]
            if not tag_data.empty:
                peak_year = tag_data.groupby('publish_year').size().idxmax()
                peak_count = tag_data.groupby('publish_year').size().max()
                report.append(f"{tag:<15}: {peak_year}年 ({peak_count} 本)")
        report.append("")
        
        return "\n".join(report)
    
    def save_analysis_results(self, df: pd.DataFrame, pivot_table: pd.DataFrame, report: str):
        """保存分析结果"""
        # 保存数据到CSV
        df.to_csv(os.path.join(config.ANALYSIS_DIR, 'books_analysis_data.csv'), 
                 index=False, encoding='utf-8-sig')
        
        pivot_table.to_csv(os.path.join(config.ANALYSIS_DIR, 'yearly_tech_tag_stats.csv'), 
                          encoding='utf-8-sig')
        
        # 保存报告
        with open(os.path.join(config.ANALYSIS_DIR, 'analysis_report.txt'), 'w', 
                 encoding='utf-8') as f:
            f.write(report)
        
        print(f"分析结果已保存到: {config.ANALYSIS_DIR}")
    
    def run_analysis(self, filename: str = "classified_books.json"):
        """运行完整的数据分析"""
        print("开始数据分析...")
        
        # 加载数据
        books = self.load_classified_books(filename)
        if not books:
            print("没有找到分类数据，请先运行数据抓取和分类")
            return
        
        # 准备数据
        df = self.prepare_data(books)
        if df.empty:
            print("没有有效的出版日期数据")
            return
        
        # 分析数据
        pivot_table = self.analyze_publications_by_year(df)
        
        # 生成可视化
        self.create_visualizations(df, pivot_table)
        
        # 生成报告
        report = self.generate_statistics_report(df, pivot_table)
        
        # 保存结果
        self.save_analysis_results(df, pivot_table, report)
        
        # 打印报告
        print("\n" + report)
        
        print("数据分析完成！")

if __name__ == "__main__":
    analyzer = DataAnalyzer()
    analyzer.run_analysis() 