import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
OPENAI_API_KEY = ''
GEMINI_API_KEY = ''

# 默认AI服务选择 ('openai' 或 'gemini')
# DEFAULT_AI_SERVICE = 'openai'
DEFAULT_AI_SERVICE = 'gemini'

# 图灵网站API配置
ITURING_BASE_URL = "https://api.ituring.com.cn/api"
SEARCH_URL = f"{ITURING_BASE_URL}/Search/Advanced"
BOOK_DETAIL_URL = f"{ITURING_BASE_URL}/Book"

# 请求配置
REQUEST_DELAY = 5  # 请求间隔时间（秒）

# 数据存储配置
DATA_DIR = "data"
BOOKS_DIR = os.path.join(DATA_DIR, "books")
ANALYSIS_DIR = os.path.join(DATA_DIR, "analysis")

# 技术标签分类
TECH_CATEGORIES = [
    "JavaScript", "Python", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift",
    "AI", "机器学习", "深度学习", "大模型", "自然语言处理", "计算机视觉",
    "数据库", "MySQL", "PostgreSQL", "MongoDB", "Redis",
    "前端开发", "后端开发", "移动开发", "DevOps", "云计算",
    "数据结构", "算法", "系统设计", "网络编程", "安全",
    "其他"
] 