#!/usr/bin/env python3
"""
arXiv 爬虫演示脚本
展示主要功能的使用方法
"""

from arxiv_crawler import ArxivCrawler
import time

def demo_basic_crawler():
    """演示基本爬虫功能"""
    print("=" * 60)
    print("演示1: 基本爬虫功能")
    print("=" * 60)
    
    crawler = ArxivCrawler(delay=1.0)
    
    # 获取AI领域的论文
    print("正在获取 cs.AI 栏目的论文...")
    papers = crawler.get_papers_from_category('cs.AI', max_papers=5)
    
    if papers:
        print(f"✓ 成功获取 {len(papers)} 篇论文")
        
        # 显示前3篇论文
        print("\n前3篇论文:")
        for i, paper in enumerate(papers[:3], 1):
            print(f"{i}. {paper['title'][:60]}...")
            print(f"   arXiv ID: {paper['arxiv_id']}")
            print(f"   作者: {', '.join(paper['authors'][:2])}{'...' if len(paper['authors']) > 2 else ''}")
            print()
        
        # 提取关键词
        keywords = crawler.extract_keywords(papers, top_n=10)
        print("前10个关键词:")
        for i, (word, count) in enumerate(keywords, 1):
            print(f"{i:2d}. {word:<15} ({count} 次)")
        
        # 保存结果
        crawler.save_papers_info(papers, 'demo_ai_papers.json')
        print(f"\n✓ 论文信息已保存到 demo_ai_papers.json")
    
    return papers

def demo_enhanced_crawler():
    """演示增强版爬虫功能"""
    print("\n" + "=" * 60)
    print("演示2: 增强版爬虫功能")
    print("=" * 60)
    
    crawler = EnhancedArxivCrawler()
    
    # 显示可用栏目
    categories = crawler.get_available_categories()
    print("可用栏目:")
    for code, name in list(categories.items())[:5]:
        print(f"  {code}: {name}")
    
    # 获取计算机视觉论文
    print(f"\n正在获取 cs.CV 栏目的论文...")
    papers = crawler.get_papers_from_category('cs.CV', max_papers=3)
    
    if papers:
        print(f"✓ 成功获取 {len(papers)} 篇论文")
        
        # 提取关键词
        keywords = crawler.extract_keywords_advanced(papers, top_n=8)
        print("\n前8个关键词:")
        for i, (word, count) in enumerate(keywords, 1):
            print(f"{i}. {word:<15} ({count} 次)")
        
        # 生成分析报告
        report = crawler.generate_report(papers, keywords, 'cs.CV')
        print(f"\n✓ 分析报告预览:")
        print("-" * 40)
        print(report[:300] + "..." if len(report) > 300 else report)
        
        # 保存报告
        with open('demo_cv_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✓ 完整报告已保存到 demo_cv_report.md")
    
    return papers

def demo_pagination():
    """演示分页功能"""
    print("\n" + "=" * 60)
    print("演示3: 分页功能")
    print("=" * 60)
    
    crawler = ArxivCrawler(delay=1.0)
    
    # 获取第1页的论文
    print("获取第1页论文...")
    papers_page1 = crawler.get_papers_from_category('cs.LG', max_papers=3, start_page=0)
    
    # 获取第2页的论文
    print("获取第2页论文...")
    papers_page2 = crawler.get_papers_from_category('cs.LG', max_papers=3, start_page=1)
    
    if papers_page1 and papers_page2:
        print(f"✓ 第1页获取到 {len(papers_page1)} 篇论文")
        print(f"✓ 第2页获取到 {len(papers_page2)} 篇论文")
        
        # 检查是否是不同的论文
        ids_page1 = {p['arxiv_id'] for p in papers_page1}
        ids_page2 = {p['arxiv_id'] for p in papers_page2}
        
        if ids_page1 != ids_page2:
            print("✓ 分页功能正常，获取到不同页面的论文")
        else:
            print("⚠ 获取到相同论文，可能是页面内容相同")
        
        print("\n第1页论文ID:", list(ids_page1))
        print("第2页论文ID:", list(ids_page2))

def demo_download_simulation():
    """演示下载功能（模拟）"""
    print("\n" + "=" * 60)
    print("演示4: 下载功能（模拟）")
    print("=" * 60)
    
    crawler = ArxivCrawler(delay=1.0)
    
    # 获取少量论文用于演示
    papers = crawler.get_papers_from_category('cs.AI', max_papers=3)
    
    if papers:
        print(f"准备下载 {len(papers)} 篇论文的PDF...")
        
        for i, paper in enumerate(papers, 1):
            print(f"{i}. {paper['title'][:50]}...")
            print(f"   PDF URL: {paper['pdf_url']}")
            
            # 这里只是演示，不实际下载
            print("   [模拟下载] 跳过实际下载以避免网络负载")
            print()
        
        print("✓ 下载功能演示完成")
        print("  实际使用时请使用 --download 参数")

def main():
    """主演示函数"""
    print("arXiv 论文爬取和下载工具 - 功能演示")
    print("=" * 60)
    
    try:
        # 演示1: 基本功能
        papers1 = demo_basic_crawler()
        
        # 演示2: 增强版功能
        papers2 = demo_enhanced_crawler()
        
        # 演示3: 分页功能
        demo_pagination()
        
        # 演示4: 下载功能
        demo_download_simulation()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("=" * 60)
        print("\n生成的文件:")
        print("- demo_ai_papers.json: AI论文信息")
        print("- demo_cv_report.md: 计算机视觉分析报告")
        print("\n使用方法:")
        print("1. 基本使用: python arxiv_crawler.py --category cs.AI --max-papers 50")
        print("2. 下载PDF: python arxiv_crawler.py --category cs.CV --max-papers 20 --download")
        print("3. 增强版: python enhanced_arxiv_crawler.py --category cs.LG --max-papers 100 --report")
        print("4. 交互式: python quick_start.py")
        
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")
        print("请检查网络连接和依赖安装")

if __name__ == "__main__":
    main()