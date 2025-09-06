#!/usr/bin/env python3
"""
多栏目爬取使用示例
展示如何使用 arxiv_crawler.py 进行多栏目爬取
"""

import subprocess
import sys

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"示例: {description}")
    print(f"命令: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 执行成功")
            # 显示部分输出
            lines = result.stdout.split('\n')
            for line in lines[:10]:  # 只显示前10行
                if line.strip():
                    print(line)
            if len(lines) > 10:
                print("... (输出已截断)")
        else:
            print(f"❌ 执行失败: {result.stderr}")
    except Exception as e:
        print(f"❌ 执行出错: {e}")

def main():
    """运行多栏目爬取示例"""
    print("arXiv 多栏目爬取使用示例")
    print("=" * 60)
    
    examples = [
        {
            "cmd": "python arxiv_crawler.py --category cs.AI cs.CV --max-papers 10 --keywords 8",
            "desc": "基本多栏目爬取 - 爬取AI和计算机视觉栏目，每栏目5篇论文"
        },
        {
            "cmd": "python arxiv_crawler.py --category cs.AI cs.CV cs.LG --max-papers 15 --wordcloud --keywords 10",
            "desc": "多栏目爬取+词云 - 爬取3个栏目并生成综合词云"
        },
        {
            "cmd": "python arxiv_crawler.py --category cs.AI cs.CV --max-papers 20 --download --keywords 12",
            "desc": "多栏目爬取+下载 - 爬取2个栏目并下载PDF文件"
        },
        {
            "cmd": "python arxiv_crawler.py --category cs.AI cs.CV cs.LG cs.RO --max-papers 24 --wordcloud --wordcloud-file multi_wordcloud.png --max-words 80",
            "desc": "多栏目爬取+自定义词云 - 爬取4个栏目并生成自定义词云"
        }
    ]
    
    print("注意: 这些示例会实际爬取论文，请确保网络连接正常")
    print("按 Ctrl+C 可以随时中断")
    
    try:
        for i, example in enumerate(examples, 1):
            print(f"\n\n示例 {i}/{len(examples)}")
            run_command(example["cmd"], example["desc"])
            
            if i < len(examples):
                input("\n按 Enter 继续下一个示例，或 Ctrl+C 退出...")
                
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n执行过程中出现错误: {e}")
    
    print(f"\n{'='*60}")
    print("多栏目爬取示例完成！")
    print("\n生成的文件:")
    print("- multi_category_papers.json: 多栏目论文信息")
    print("- wordcloud.png: 综合词云图片")
    print("- papers/: PDF文件下载目录（如果启用下载）")

if __name__ == "__main__":
    main()