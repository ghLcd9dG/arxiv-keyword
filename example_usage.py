#!/usr/bin/env python3
"""
arXiv 爬虫使用示例
演示如何使用 arXiv 爬虫工具
"""

from arxiv_crawler import ArxivCrawler
from enhanced_arxiv_crawler import EnhancedArxivCrawler
import json

def basic_example():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建爬虫实例
    crawler = ArxivCrawler(delay=1.0)
    
    # 获取最近50篇AI论文
    papers = crawler.get_papers_from_category('cs.AI', max_papers=50)
    
    print(f"获取到 {len(papers)} 篇论文")
    
    # 提取关键词
    keywords = crawler.extract_keywords(papers, top_n=10)
    print("\n前10个关键词:")
    for i, (word, count) in enumerate(keywords, 1):
        print(f"{i}. {word} ({count} 次)")
    
    # 保存论文信息
    crawler.save_papers_info(papers, 'ai_papers.json')
    print("\n论文信息已保存到 ai_papers.json")

def enhanced_example():
    """增强版使用示例"""
    print("\n=== 增强版使用示例 ===")
    
    # 创建增强版爬虫实例
    crawler = EnhancedArxivCrawler('config.json')
    
    # 显示可用栏目
    categories = crawler.get_available_categories()
    print("可用栏目:")
    for code, name in list(categories.items())[:5]:  # 只显示前5个
        print(f"  {code}: {name}")
    
    # 获取计算机视觉论文
    papers = crawler.get_papers_from_category('cs.CV', max_papers=30)
    
    print(f"\n获取到 {len(papers)} 篇计算机视觉论文")
    
    # 提取关键词
    keywords = crawler.extract_keywords_advanced(papers, top_n=15)
    print("\n前15个关键词:")
    for i, (word, count) in enumerate(keywords, 1):
        print(f"{i:2d}. {word:<20} ({count} 次)")
    
    # 生成分析报告
    report = crawler.generate_report(papers, keywords, 'cs.CV')
    print(f"\n=== 分析报告预览 ===")
    print(report[:500] + "..." if len(report) > 500 else report)

def batch_processing_example():
    """批量处理示例"""
    print("\n=== 批量处理示例 ===")
    
    crawler = EnhancedArxivCrawler('config.json')
    
    # 处理多个栏目
    categories = ['cs.AI', 'cs.CV', 'cs.LG']
    all_keywords = {}
    
    for category in categories:
        print(f"\n处理栏目: {category}")
        papers = crawler.get_papers_from_category(category, max_papers=20)
        
        if papers:
            keywords = crawler.extract_keywords_advanced(papers, top_n=10)
            all_keywords[category] = keywords
            
            print(f"  - 获取到 {len(papers)} 篇论文")
            print(f"  - 前5个关键词: {[word for word, _ in keywords[:5]]}")
    
    # 保存所有结果
    with open('batch_results.json', 'w', encoding='utf-8') as f:
        json.dump(all_keywords, f, ensure_ascii=False, indent=2)
    
    print(f"\n批量处理结果已保存到 batch_results.json")

def download_example():
    """下载示例"""
    print("\n=== 下载示例 ===")
    
    crawler = ArxivCrawler(delay=0.5)  # 较短的延迟用于演示
    
    # 获取少量论文用于下载演示
    papers = crawler.get_papers_from_category('cs.AI', max_papers=5)
    
    if papers:
        print(f"准备下载 {len(papers)} 篇论文...")
        
        # 下载论文（实际使用时请谨慎，避免下载过多文件）
        success_count = crawler.download_papers(papers, 'demo_papers', max_downloads=3)
        print(f"成功下载 {success_count} 篇论文到 demo_papers/ 目录")

if __name__ == "__main__":
    try:
        # 运行基本示例
        basic_example()
        
        # 运行增强版示例
        enhanced_example()
        
        # 运行批量处理示例
        batch_processing_example()
        
        # 运行下载示例（可选，会实际下载文件）
        # download_example()
        
        print("\n=== 所有示例运行完成 ===")
        
    except Exception as e:
        print(f"示例运行出错: {e}")
        print("请确保已安装所需依赖: pip install -r requirements.txt")