import openai
import json
import os
import time
from typing import List, Dict, Any
from tqdm import tqdm
import config

try:
    import google.generativeai as genai
except ImportError:
    print("警告: 未安装google-generativeai库，Gemini功能将不可用")
    genai = None

class BookClassifier:
    def __init__(self, ai_service: str = None):
        """
        初始化图书分类器
        
        Args:
            ai_service: AI服务选择，'openai' 或 'gemini'，默认为config.DEFAULT_AI_SERVICE
        """
        self.ai_service = ai_service or config.DEFAULT_AI_SERVICE
        
        if self.ai_service == 'openai':
            self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        elif self.ai_service == 'gemini':
            if genai is None:
                raise ImportError("请安装google-generativeai库: pip install google-generativeai")
            genai.configure(api_key=config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            raise ValueError(f"不支持的AI服务: {self.ai_service}，请选择 'openai' 或 'gemini'")
    
    def classify_book(self, book: Dict[str, Any]) -> str:
        """为单本图书分配技术标签"""
        # 提取图书的关键信息
        name = book.get('name', '')
        abstract = book.get('abstract', '')
        brief_intro = book.get('briefIntro', {})
        highlight = brief_intro.get('highlight', '')
        author_info = brief_intro.get('authorInfo', '')
        tags = book.get('tags', [])
        categories = book.get('categories', [])
        
        # 构建用于分类的文本
        classification_text = f"""
书名: {name}
简介: {abstract}
亮点: {highlight}
作者信息: {author_info}
标签: {', '.join([tag.get('name', '') for tag in tags])}
分类: {', '.join([cat.get('name', '') for cat_list in categories for cat in cat_list])}
        """.strip()
        
        # 构建提示词
        prompt = f"""
请根据以下图书信息，从以下技术标签中选择最合适的一个标签：

技术标签列表：
{', '.join(config.TECH_CATEGORIES)}

图书信息：
{classification_text}

请只返回一个标签名称，不要包含任何其他文字。如果以上标签都不合适，请返回"其他"。
        """
        
        try:
            if self.ai_service == 'openai':
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一个专业的图书分类助手，擅长为技术类图书分配准确的技术标签。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    temperature=0.1
                )
                classification = response.choices[0].message.content.strip()
                
            elif self.ai_service == 'gemini':
                response = self.model.generate_content(
                    f"你是一个专业的图书分类助手，擅长为技术类图书分配准确的技术标签。\n\n{prompt}"
                )
                classification = response.text.strip()
            
            # 验证返回的标签是否在预定义列表中
            if classification not in config.TECH_CATEGORIES:
                classification = "其他"
            
            return classification
            
        except Exception as e:
            print(f"分类失败: {e}")
            return "其他"
    
    def classify_books_batch(self, books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量分类图书"""
        classified_books = []
        
        print(f"开始为图书分配技术标签 (使用 {self.ai_service.upper()} API)...")
        
        for i, book in enumerate(tqdm(books, desc="分类图书")):
            # 为图书添加技术标签
            tech_tag = self.classify_book(book)
            book['tech_tag'] = tech_tag
            
            classified_books.append(book)
            
            # 添加延迟以避免API限制
            if i < len(books) - 1:  # 不是最后一本书
                time.sleep(1)
        
        return classified_books
    
    def save_classified_books(self, books: List[Dict[str, Any]], filename: str = "classified_books.json"):
        """保存已分类的图书数据"""
        filepath = os.path.join(config.BOOKS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        
        print(f"已分类的图书数据已保存到: {filepath}")
    
    def load_classified_books(self, filename: str = "classified_books.json") -> List[Dict[str, Any]]:
        """加载已分类的图书数据"""
        filepath = os.path.join(config.BOOKS_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"分类数据文件不存在: {filepath}")
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

if __name__ == "__main__":
    # 测试分类器
    print("测试OpenAI分类器...")
    classifier_openai = BookClassifier(ai_service='openai')
    
    # 示例图书数据
    test_book = {
        "name": "Python深度学习",
        "abstract": "本书介绍Python深度学习的基础知识和实践应用",
        "briefIntro": {
            "highlight": "Python深度学习入门指南",
            "authorInfo": "深度学习专家"
        },
        "tags": [{"name": "Python"}, {"name": "深度学习"}],
        "categories": [[{"name": "计算机"}, {"name": "人工智能"}]]
    }
    
    tag = classifier_openai.classify_book(test_book)
    print(f"OpenAI测试图书分类结果: {tag}")
    
    # 测试Gemini分类器（如果可用）
    if genai is not None:
        print("\n测试Gemini分类器...")
        try:
            classifier_gemini = BookClassifier(ai_service='gemini')
            tag = classifier_gemini.classify_book(test_book)
            print(f"Gemini测试图书分类结果: {tag}")
        except Exception as e:
            print(f"Gemini测试失败: {e}")
    else:
        print("\nGemini不可用，跳过测试") 