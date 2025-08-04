# 快速启动指南

## 🚀 5分钟快速开始

### 1. 自动安装（推荐）

```bash
# 运行自动安装脚本
python setup.py
```

### 2. 手动安装

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行测试

```bash
# 测试项目功能
python test_project.py
```

### 4. 开始使用

#### 小规模测试（推荐首次使用）

```bash
# 抓取前3页数据（约15本图书）
python main.py --max-pages 3
```

#### 完整运行

```bash
# 抓取所有数据（可能需要较长时间）
python main.py
```

#### 分步运行

```bash
# 仅抓取数据
python main.py --scrape-only --max-pages 5

# 仅进行分类
python main.py --classify-only

# 仅进行分析
python main.py --analyze-only
```

## 📊 查看结果

运行完成后，查看以下文件：

### 数据文件
- `data/books/books_data.json` - 原始图书数据
- `data/books/classified_books.json` - 已分类的图书数据

### 分析结果
- `data/analysis/analysis_report.txt` - 详细分析报告
- `data/analysis/books_analysis_data.csv` - 分析数据表格

### 可视化图表
- `data/analysis/tech_tag_distribution.png` - 技术标签分布
- `data/analysis/yearly_tech_tag_trend.png` - 年度趋势图
- `data/analysis/tech_tag_year_heatmap.png` - 热力图
- `data/analysis/yearly_total_publications.png` - 年度总量图

## ⚠️ 注意事项

1. **网络连接**: 确保可以访问图灵网站
2. **API费用**: 使用OpenAI API会产生费用
3. **时间成本**: 完整抓取可能需要1-2小时
4. **数据完整性**: 建议在稳定网络环境下运行

## 🔧 故障排除

### 常见问题

1. **模块导入错误**
   ```bash
   # 确保在虚拟环境中
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. **网络连接错误**
   - 检查网络连接
   - 尝试使用VPN
   - 减少抓取页数进行测试

3. **API密钥错误**
   - 检查config.py中的API密钥配置
   - 确保OpenAI账户有足够余额

4. **字体显示问题**
   - Windows: 安装SimHei字体
   - macOS: 安装Microsoft YaHei字体

### 调试模式

```bash
# 使用最小数据量测试
python main.py --max-pages 1

# 查看详细帮助
python main.py --help
```

## 📈 预期结果

运行完成后，您将获得：

- 图灵图书的完整技术分类数据
- 各技术领域的年度出版趋势分析
- 多种可视化图表展示
- 详细的统计报告

## 🎯 下一步

1. 查看生成的图表和报告
2. 根据分析结果调整技术标签分类
3. 定期运行更新数据
4. 自定义分析维度

---

**提示**: 首次使用建议先运行小规模测试，确认一切正常后再进行完整数据抓取。 