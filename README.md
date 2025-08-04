# 图灵图书数据抓取与分析系统

这是一个用于抓取图灵图书网站数据并进行技术标签分析和可视化的Python项目。

## 功能特性

- 🔍 **数据抓取**: 自动抓取图灵图书网站的图书信息
- 🏷️ **智能分类**: 使用AI模型（OpenAI GPT或Google Gemini）为图书分配技术标签
- 📊 **数据分析**: 统计各技术标签的年度出版趋势
- 📈 **可视化**: 生成多种图表展示分析结果
- 💾 **数据存储**: 将数据保存为JSON格式供离线分析

## 项目结构

```
ituring-book-analyse/
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── data_scraper.py      # 数据抓取模块
├── book_classifier.py   # 图书分类模块
├── data_analyzer.py     # 数据分析模块
├── test_project.py      # 功能测试脚本
├── test_ai_services.py  # AI服务测试脚本
├── requirements.txt     # 项目依赖
├── README.md           # 项目说明
├── instruction.md      # 需求文档
└── data/               # 数据存储目录
    ├── books/          # 图书数据
    └── analysis/       # 分析结果
```

## 安装说明

### 1. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

项目支持两种AI服务进行图书分类：

- **OpenAI GPT**: 使用GPT-3.5-turbo模型
- **Google Gemini**: 使用Gemini Pro模型

API密钥已在代码中配置，如需修改请编辑 `config.py` 文件。

## 使用方法

### 完整流程运行

运行完整的数据抓取、分类和分析流程：

```bash
# 使用默认AI服务（OpenAI）
python main.py

# 指定使用OpenAI
python main.py --ai-service openai

# 指定使用Gemini
python main.py --ai-service gemini
```

### 分步运行

#### 仅抓取数据

```bash
python main.py --scrape-only --max-pages 5
```

#### 仅进行分类

```bash
# 使用默认AI服务
python main.py --classify-only

# 指定AI服务
python main.py --classify-only --ai-service gemini
```

#### 仅进行分析

```bash
python main.py --analyze-only
```

### 参数说明

- `--max-pages`: 限制抓取的最大页数（默认抓取所有页面）
- `--ai-service`: 选择AI服务，可选值：`openai` 或 `gemini`（默认：openai）
- `--scrape-only`: 仅执行数据抓取
- `--classify-only`: 仅执行图书分类
- `--analyze-only`: 仅执行数据分析

## 测试功能

### 运行完整测试

```bash
# 使用默认AI服务测试
python test_project.py

# 指定AI服务测试
python test_project.py --ai-service gemini
```

### 测试AI服务

```bash
python test_ai_services.py
```

这个脚本会测试OpenAI和Gemini两种AI服务是否正常工作。

## 输出结果

### 数据文件

- `data/books/books_data.json`: 原始图书数据
- `data/books/classified_books.json`: 已分类的图书数据

### 分析结果

- `data/analysis/books_analysis_data.csv`: 分析数据表格
- `data/analysis/yearly_tech_tag_stats.csv`: 年度技术标签统计
- `data/analysis/analysis_report.txt`: 分析报告

### 可视化图表

- `data/analysis/tech_tag_distribution.png`: 技术标签分布饼图
- `data/analysis/yearly_tech_tag_trend.png`: 年度技术标签趋势图
- `data/analysis/tech_tag_year_heatmap.png`: 技术标签年度热力图
- `data/analysis/yearly_total_publications.png`: 年度出版总量趋势图

## 技术标签分类

系统支持以下技术标签分类：

- **编程语言**: JavaScript, Python, Java, C++, C#, Go, Rust, PHP, Ruby, Swift
- **AI相关**: AI, 机器学习, 深度学习, 大模型, 自然语言处理, 计算机视觉
- **数据库**: 数据库, MySQL, PostgreSQL, MongoDB, Redis
- **开发领域**: 前端开发, 后端开发, 移动开发, DevOps, 云计算
- **计算机基础**: 数据结构, 算法, 系统设计, 网络编程, 安全
- **其他**: 其他

## AI服务对比

| 特性 | OpenAI GPT | Google Gemini |
|------|------------|---------------|
| 模型 | GPT-3.5-turbo | Gemini Pro |
| 响应速度 | 较快 | 较快 |
| 中文支持 | 优秀 | 优秀 |
| 费用 | 按token计费 | 按token计费 |
| 稳定性 | 高 | 高 |

## 注意事项

1. **请求频率**: 程序设置了5秒的请求间隔，以避免被网站防火墙拦截
2. **API费用**: 使用AI API会产生费用，请注意控制使用量
3. **数据完整性**: 建议在稳定的网络环境下运行，确保数据抓取的完整性
4. **中文字体**: 图表生成需要系统中文字体支持
5. **依赖库**: 确保安装了所有必要的依赖库，特别是 `google-generativeai`

## 故障排除

### 常见问题

1. **网络连接错误**: 检查网络连接，确保可以访问图灵网站
2. **API密钥错误**: 确认AI服务API密钥配置正确
3. **字体显示问题**: 安装中文字体或修改matplotlib字体配置
4. **权限错误**: 确保程序有写入数据目录的权限
5. **Gemini导入错误**: 运行 `pip install google-generativeai` 安装依赖

### 调试模式

如需调试，可以修改 `config.py` 中的 `REQUEST_DELAY` 参数，或使用较小的 `max_pages` 值进行测试。

### AI服务测试

如果遇到AI服务问题，可以运行：

```bash
python test_ai_services.py
```

这个脚本会详细测试两种AI服务的功能。

## 许可证

本项目仅供学习和研究使用，请遵守相关网站的使用条款。

## 贡献

欢迎提交Issue和Pull Request来改进项目。 