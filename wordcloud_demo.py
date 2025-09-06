#!/usr/bin/env python3
"""
词云功能演示脚本
展示如何使用 arXiv 爬虫生成词云
"""

from arxiv_crawler import ArxivCrawler
import os

def demo_wordcloud_basic():
    """基本词云演示"""
    print("=== 基本词云演示 ===")
    
    crawler = ArxivCrawler()
    
    # 爬取论文
    papers = crawler.get_papers_from_category('cs.AI', max_papers=20)
    
    if papers:
        # 生成基本词云
        success = crawler.generate_wordcloud(papers, 'basic_wordcloud.png')
        if success:
            print("✅ 基本词云生成成功: basic_wordcloud.png")
        else:
            print("❌ 基本词云生成失败")
    else:
        print("❌ 没有获取到论文")

def demo_wordcloud_custom():
    """自定义词云演示"""
    print("\n=== 自定义词云演示 ===")
    
    crawler = ArxivCrawler()
    
    # 爬取计算机视觉论文
    papers = crawler.get_papers_from_category('cs.CV', max_papers=25)
    
    if papers:
        # 生成自定义词云
        success = crawler.generate_wordcloud(
            papers, 
            'custom_wordcloud.png',
            max_words=80,
            width=1000,
            height=500
        )
        if success:
            print("✅ 自定义词云生成成功: custom_wordcloud.png")
        else:
            print("❌ 自定义词云生成失败")
    else:
        print("❌ 没有获取到论文")

def demo_wordcloud_multiple_categories():
    """多栏目词云演示"""
    print("\n=== 多栏目词云演示 ===")
    
    crawler = ArxivCrawler()
    categories = ['cs.AI', 'cs.CV', 'cs.LG']
    
    for category in categories:
        print(f"\n处理栏目: {category}")
        papers = crawler.get_papers_from_category(category, max_papers=15)
        
        if papers:
            filename = f"{category}_wordcloud.png"
            success = crawler.generate_wordcloud(
                papers, 
                filename,
                max_words=60,
                width=800,
                height=400
            )
            if success:
                print(f"✅ {category} 词云生成成功: {filename}")
            else:
                print(f"❌ {category} 词云生成失败")
        else:
            print(f"❌ {category} 没有获取到论文")

def demo_wordcloud_with_keywords():
    """词云与关键词对比演示"""
    print("\n=== 词云与关键词对比演示 ===")
    
    crawler = ArxivCrawler()
    
    # 爬取机器学习论文
    papers = crawler.get_papers_from_category('cs.LG', max_papers=30)
    
    if papers:
        # 提取关键词
        keywords = crawler.extract_keywords(papers, top_n=15)
        print("\n前15个关键词:")
        for i, (word, count) in enumerate(keywords, 1):
            print(f"{i:2d}. {word:15s} ({count} 次)")
        
        # 生成词云
        success = crawler.generate_wordcloud(
            papers, 
            'ml_wordcloud.png',
            max_words=100,
            width=1200,
            height=600
        )
        if success:
            print("\n✅ 机器学习词云生成成功: ml_wordcloud.png")
        else:
            print("\n❌ 机器学习词云生成失败")
    else:
        print("❌ 没有获取到论文")

def show_generated_files():
    """显示生成的文件"""
    print("\n=== 生成的文件 ===")
    
    png_files = [f for f in os.listdir('.') if f.endswith('.png')]
    
    if png_files:
        print("生成的词云文件:")
        for file in sorted(png_files):
            size = os.path.getsize(file)
            print(f"  📄 {file} ({size:,} bytes)")
    else:
        print("没有找到词云文件")

def main():
    """运行所有演示"""
    print("arXiv 词云功能演示")
    print("=" * 50)
    
    try:
        demo_wordcloud_basic()
        demo_wordcloud_custom()
        demo_wordcloud_multiple_categories()
        demo_wordcloud_with_keywords()
        show_generated_files()
        
        print("\n" + "=" * 50)
        print("🎉 词云演示完成！")
        print("\n命令行使用示例:")
        print("python arxiv_crawler.py --category cs.AI --max-papers 50 --wordcloud")
        print("python arxiv_crawler.py --category cs.CV --max-papers 30 --wordcloud --wordcloud-file cv.png --max-words 80")
        
    except KeyboardInterrupt:
        print("\n\n演示被用户中断")
    except Exception as e:
        print(f"\n演示过程中出现错误: {e}")

if __name__ == "__main__":
    main()