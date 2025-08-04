import requests
import json
import time
import os
from typing import List, Dict, Any
from tqdm import tqdm
import config

class IturingScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # 确保数据目录存在
        os.makedirs(config.BOOKS_DIR, exist_ok=True)
        os.makedirs(config.ANALYSIS_DIR, exist_ok=True)
    
    def get_book_list(self, page: int = 1, category_id: int = 0, sort: str = "new") -> Dict[str, Any]:
        """获取图书列表"""
        payload = {
            "categoryId": category_id,
            "sort": sort,
            "page": page,
            "name": "",
            "edition": 1
        }
        
        try:
            response = self.session.post(config.SEARCH_URL, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取图书列表失败 (页面 {page}): {e}")
            return {"bookItems": [], "pagination": {"pageCount": 0}}
    
    def get_book_detail(self, book_id: int) -> Dict[str, Any]:
        """获取单本图书详细信息"""
        url = f"{config.BOOK_DETAIL_URL}/{book_id}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"获取图书详情失败 (ID: {book_id}): {e}")
            return {}
    
    def scrape_all_books(self, max_pages: int = None) -> List[Dict[str, Any]]:
        """抓取所有图书数据"""
        all_books = []
        
        # 获取第一页来确定总页数
        first_page = self.get_book_list(page=1)
        total_pages = first_page.get("pagination", {}).get("pageCount", 0)
        
        if max_pages:
            total_pages = min(total_pages, max_pages)
        
        print(f"开始抓取图书数据，总共 {total_pages} 页")
        
        for page in tqdm(range(1, total_pages + 1), desc="抓取图书列表"):
            page_data = self.get_book_list(page=page)
            book_items = page_data.get("bookItems", [])
            
            for book in book_items:
                book_id = book.get("id")
                if book_id:
                    print(f"正在获取图书详情: {book.get('name', 'Unknown')} (ID: {book_id})")
                    
                    # 获取详细信息
                    detail = self.get_book_detail(book_id)
                    if detail:
                        # 合并基础信息和详细信息
                        book.update(detail)
                        all_books.append(book)
                    
                    # 请求间隔
                    time.sleep(config.REQUEST_DELAY)
            
            # 页面间隔
            time.sleep(config.REQUEST_DELAY)
        
        return all_books
    
    def save_books_data(self, books: List[Dict[str, Any]], filename: str = "books_data.json"):
        """保存图书数据到JSON文件"""
        filepath = os.path.join(config.BOOKS_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        
        print(f"图书数据已保存到: {filepath}")
        print(f"总共保存了 {len(books)} 本图书的数据")
    
    def load_books_data(self, filename: str = "books_data.json") -> List[Dict[str, Any]]:
        """从JSON文件加载图书数据"""
        filepath = os.path.join(config.BOOKS_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"数据文件不存在: {filepath}")
            return []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

if __name__ == "__main__":
    scraper = IturingScraper()
    
    # 抓取所有图书数据（限制页数以避免长时间运行）
    books = scraper.scrape_all_books(max_pages=5)  # 可以调整页数
    
    # 保存数据
    scraper.save_books_data(books) 