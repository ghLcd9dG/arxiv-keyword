#!/usr/bin/env python3
"""
arXiv 论文爬取和下载工具
支持从特定栏目提取关键词并下载最近论文
"""

import requests
import re
import os
import time
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import Counter
import json
from typing import List, Dict, Optional
import logging
from pathlib import Path

# 词云相关导入
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("警告: 词云功能需要安装 wordcloud 和 matplotlib 包")
    print("请运行: pip install wordcloud matplotlib")

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ArxivCrawler:
    def __init__(self, base_url: str = "https://arxiv.org", delay: float = 1.0):
        """
        初始化 arXiv 爬虫
        
        Args:
            base_url: arXiv 基础 URL
            delay: 请求间隔时间（秒）
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
    def get_papers_from_category(self, category: str, max_papers: int = 50, 
                                start_page: int = 0) -> List[Dict]:
        """
        从指定栏目获取论文列表
        
        Args:
            category: 栏目代码，如 'cs.AI', 'cs.CV' 等
            max_papers: 最大论文数量
            start_page: 起始页码
            
        Returns:
            论文信息列表
        """
        papers = []
        page = start_page
        items_per_page = 50  # arXiv 每页显示50篇论文
        
        logger.info(f"开始爬取栏目 {category} 的论文，目标数量: {max_papers}")
        
        while len(papers) < max_papers:
            # 构建分页 URL
            url = f"{self.base_url}/list/{category}/recent"
            if page > 0:
                url += f"?skip={page * items_per_page}"
                
            logger.info(f"正在爬取第 {page + 1} 页: {url}")
            
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                page_papers = self._parse_paper_list(soup)
                
                if not page_papers:
                    logger.info("没有更多论文，停止爬取")
                    break
                    
                papers.extend(page_papers)
                logger.info(f"第 {page + 1} 页获取到 {len(page_papers)} 篇论文，总计: {len(papers)}")
                
                # 如果当前页论文数少于预期，说明已经到最后一页
                if len(page_papers) < items_per_page:
                    logger.info("已到达最后一页")
                    break
                    
                page += 1
                time.sleep(self.delay)  # 避免请求过于频繁
                
            except requests.RequestException as e:
                logger.error(f"请求失败: {e}")
                break
                
        # 限制返回的论文数量
        return papers[:max_papers]
    
    def _parse_paper_list(self, soup: BeautifulSoup) -> List[Dict]:
        """解析论文列表页面"""
        papers = []
        
        # 查找论文条目 - 使用dl结构
        dl_elements = soup.find_all('dl')
        for dl in dl_elements:
            # 查找dt和dd对
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            
            for dt, dd in zip(dt_elements, dd_elements):
                try:
                    paper_info = self._extract_paper_info(dt, dd)
                    if paper_info:
                        papers.append(paper_info)
                except Exception as e:
                    logger.warning(f"解析论文信息失败: {e}")
                    continue
        
        return papers
    
    def _extract_paper_info(self, dt, dd) -> Optional[Dict]:
        """从dt和dd元素提取论文信息"""
        try:
            # 从dt元素提取arXiv ID和PDF链接
            arxiv_id = ""
            pdf_url = ""
            
            # 查找arXiv ID链接
            arxiv_link = dt.find('a', href=re.compile(r'/abs/'))
            if arxiv_link:
                arxiv_id = arxiv_link.get_text().strip().replace('arXiv:', '')
                pdf_url = f"{self.base_url}/pdf/{arxiv_id}.pdf"
            
            if not arxiv_id:
                return None
            
            # 从dd元素提取论文详细信息
            meta_div = dd.find('div', class_='meta')
            if not meta_div:
                return None
            
            # 提取标题
            title_elem = meta_div.find('div', class_='list-title')
            if not title_elem:
                return None
                
            title = title_elem.get_text().replace('Title:', '').strip()
            # 清理标题中的换行符和多余空格
            title = ' '.join(title.split())
            
            # 提取作者
            authors_elem = meta_div.find('div', class_='list-authors')
            authors = []
            if authors_elem:
                author_links = authors_elem.find_all('a')
                authors = [link.get_text().strip() for link in author_links]
            
            # 提取摘要
            abstract_elem = meta_div.find('p', class_='mathjax')
            abstract = ""
            if abstract_elem:
                abstract = abstract_elem.get_text().strip()
                # 清理摘要中的换行符和多余空格
                abstract = ' '.join(abstract.split())
            
            # 提取提交日期
            date_elem = meta_div.find('div', class_='list-dateline')
            date = ""
            if date_elem:
                date = date_elem.get_text().strip()
                # 提取日期部分
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date)
                if date_match:
                    date = date_match.group(1)
            
            return {
                'arxiv_id': arxiv_id,
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'date': date,
                'pdf_url': pdf_url
            }
            
        except Exception as e:
            logger.warning(f"提取论文信息时出错: {e}")
            return None
    
    def extract_keywords(self, papers: List[Dict], top_n: int = 20) -> List[tuple]:
        """
        从论文标题和摘要中提取关键词
        
        Args:
            papers: 论文列表
            top_n: 返回前N个关键词
            
        Returns:
            关键词及其频次列表
        """
        logger.info("开始提取关键词...")
        
        # 合并所有文本
        all_text = ""
        for paper in papers:
            all_text += paper['title'] + " " + paper['abstract'] + " "
        
        # 简单的关键词提取（可以后续改进为更复杂的NLP方法）
        # 移除常见停用词
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        # 提取单词（简单分词）
        words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
        
        # 过滤停用词和短词
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # 统计词频
        word_counts = Counter(filtered_words)
        
        # 返回前N个关键词
        top_keywords = word_counts.most_common(top_n)
        
        logger.info(f"提取到 {len(top_keywords)} 个关键词")
        return top_keywords
    
    def download_paper(self, paper: Dict, download_dir: str = "papers") -> bool:
        """
        下载单篇论文的PDF
        
        Args:
            paper: 论文信息字典
            download_dir: 下载目录
            
        Returns:
            是否下载成功
        """
        if not paper.get('pdf_link'):
            logger.warning(f"论文 {paper['title']} 没有PDF链接")
            return False
            
        # 创建下载目录
        Path(download_dir).mkdir(exist_ok=True)
        
        # 生成文件名
        safe_title = re.sub(r'[^\w\s-]', '', paper['title'])[:100]
        filename = f"{paper['arxiv_id']}_{safe_title}.pdf"
        filepath = os.path.join(download_dir, filename)
        
        # 如果文件已存在，跳过下载
        if os.path.exists(filepath):
            logger.info(f"文件已存在，跳过: {filename}")
            return True
            
        try:
            logger.info(f"正在下载: {paper['title']}")
            response = self.session.get(paper['pdf_link'], timeout=60)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            logger.info(f"下载完成: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"下载失败 {paper['title']}: {e}")
            return False
    
    def download_papers(self, papers: List[Dict], download_dir: str = "papers", 
                       max_downloads: Optional[int] = None) -> int:
        """
        批量下载论文
        
        Args:
            papers: 论文列表
            download_dir: 下载目录
            max_downloads: 最大下载数量
            
        Returns:
            成功下载的数量
        """
        if max_downloads:
            papers = papers[:max_downloads]
            
        logger.info(f"开始下载 {len(papers)} 篇论文到目录: {download_dir}")
        
        success_count = 0
        for i, paper in enumerate(papers, 1):
            logger.info(f"进度: {i}/{len(papers)}")
            if self.download_paper(paper, download_dir):
                success_count += 1
            time.sleep(self.delay)  # 避免请求过于频繁
            
        logger.info(f"下载完成，成功: {success_count}/{len(papers)}")
        return success_count
    
    def save_papers_info(self, papers: List[Dict], filename: str = "papers_info.json"):
        """保存论文信息到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        logger.info(f"论文信息已保存到: {filename}")
    
    def generate_wordcloud(self, papers: List[Dict], output_file: str = "wordcloud.png", 
                          max_words: int = 100, width: int = 800, height: int = 400) -> bool:
        """
        生成词云图片
        
        Args:
            papers: 论文列表
            output_file: 输出文件名
            max_words: 最大词数
            width: 图片宽度
            height: 图片高度
            
        Returns:
            是否生成成功
        """
        if not WORDCLOUD_AVAILABLE:
            logger.error("词云功能不可用，请安装 wordcloud 和 matplotlib 包")
            return False
            
        try:
            logger.info("开始生成词云...")
            
            # 合并所有文本
            all_text = ""
            for paper in papers:
                all_text += paper['title'] + " " + paper['abstract'] + " "
            
            # 简单的文本预处理
            words = re.findall(r'\b[a-zA-Z]{3,}\b', all_text.lower())
            
            # 过滤停用词
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
                'before', 'after', 'above', 'below', 'between', 'among', 'is', 'are',
                'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
                'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
                'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
                'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
                'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
                'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
                'whose', 'where', 'when', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now',
                'using', 'used', 'use', 'based', 'approach', 'method', 'methods', 'paper', 'study',
                'research', 'work', 'works', 'propose', 'proposed', 'proposes', 'present', 'presents',
                'presented', 'show', 'shows', 'showed', 'demonstrate', 'demonstrates', 'demonstrated',
                'result', 'results', 'experiment', 'experiments', 'experimental', 'evaluation',
                'evaluate', 'evaluated', 'performance', 'model', 'models', 'algorithm', 'algorithms',
                'data', 'dataset', 'datasets', 'learning', 'learn', 'learned', 'training', 'train',
                'test', 'testing', 'tested', 'validation', 'validate', 'validated'
            }
            
            filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
            
            if not filtered_words:
                logger.warning("没有足够的词汇生成词云")
                return False
            
            # 创建词云
            wordcloud = WordCloud(
                width=width,
                height=height,
                background_color='white',
                max_words=max_words,
                colormap='viridis',
                relative_scaling=0.5,
                random_state=42
            ).generate(' '.join(filtered_words))
            
            # 保存词云图片
            plt.figure(figsize=(width/100, height/100))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"词云已保存到: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"生成词云失败: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='arXiv 论文爬取和下载工具')
    parser.add_argument('--category', '-c', nargs='+', default=['cs.AI'], 
                       help='栏目代码，支持多个栏目 (默认: cs.AI)')
    parser.add_argument('--max-papers', '-n', type=int, default=50,
                       help='最大论文数量 (默认: 50)')
    parser.add_argument('--download', '-d', action='store_true',
                       help='是否下载PDF文件')
    parser.add_argument('--download-dir', default='papers',
                       help='下载目录 (默认: papers)')
    parser.add_argument('--max-downloads', type=int,
                       help='最大下载数量')
    parser.add_argument('--keywords', '-k', type=int, default=20,
                       help='提取关键词数量 (默认: 20)')
    parser.add_argument('--delay', type=float, default=1.0,
                       help='请求间隔时间/秒 (默认: 1.0)')
    parser.add_argument('--start-page', type=int, default=0,
                       help='起始页码 (默认: 0)')
    parser.add_argument('--wordcloud', '-w', action='store_true',
                       help='生成词云图片')
    parser.add_argument('--wordcloud-file', default='wordcloud.png',
                       help='词云输出文件名 (默认: wordcloud.png)')
    parser.add_argument('--max-words', type=int, default=100,
                       help='词云最大词数 (默认: 100)')
    parser.add_argument('--wordcloud-width', type=int, default=800,
                       help='词云图片宽度 (默认: 800)')
    parser.add_argument('--wordcloud-height', type=int, default=400,
                       help='词云图片高度 (默认: 400)')
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    crawler = ArxivCrawler(delay=args.delay)
    
    try:
        all_papers = []
        all_results = {}
        
        # 处理多栏目
        if len(args.category) == 1:
            # 单栏目模式
            category = args.category[0]
            logger.info(f"开始爬取栏目 {category} 的论文，目标数量: {args.max_papers}")
            
            papers = crawler.get_papers_from_category(
                category=category,
                max_papers=args.max_papers,
                start_page=args.start_page
            )
            
            if not papers:
                logger.error("没有获取到任何论文")
                return
                
            all_papers = papers
            all_results[category] = papers
            
        else:
            # 多栏目模式
            papers_per_category = args.max_papers // len(args.category)
            if papers_per_category < 1:
                papers_per_category = 1
                
            logger.info(f"开始爬取 {len(args.category)} 个栏目的论文，每栏目目标数量: {papers_per_category}")
            
            for i, category in enumerate(args.category, 1):
                logger.info(f"[{i}/{len(args.category)}] 正在爬取栏目: {category}")
                
                papers = crawler.get_papers_from_category(
                    category=category,
                    max_papers=papers_per_category,
                    start_page=args.start_page
                )
                
                if papers:
                    all_papers.extend(papers)
                    all_results[category] = papers
                    logger.info(f"栏目 {category} 获取到 {len(papers)} 篇论文")
                else:
                    logger.warning(f"栏目 {category} 没有获取到论文")
        
        if not all_papers:
            logger.error("没有获取到任何论文")
            return
            
        logger.info(f"总共获取 {len(all_papers)} 篇论文")
        
        # 保存论文信息
        if len(args.category) == 1:
            # 单栏目：保存为 papers_info.json
            crawler.save_papers_info(all_papers)
        else:
            # 多栏目：保存为多栏目结果
            import json
            from datetime import datetime
            
            multi_result = {
                'categories': args.category,
                'total_papers': len(all_papers),
                'papers_per_category': {cat: len(papers) for cat, papers in all_results.items()},
                'all_papers': all_papers,
                'category_papers': all_results,
                'timestamp': datetime.now().isoformat()
            }
            
            with open('multi_category_papers.json', 'w', encoding='utf-8') as f:
                json.dump(multi_result, f, ensure_ascii=False, indent=2)
            logger.info("多栏目论文信息已保存到: multi_category_papers.json")
        
        # 提取关键词
        keywords = crawler.extract_keywords(all_papers, top_n=args.keywords)
        print("\n=== 关键词统计 ===")
        for word, count in keywords:
            print(f"{word}: {count}")
        
        # 生成词云
        if args.wordcloud:
            if crawler.generate_wordcloud(
                all_papers, 
                output_file=args.wordcloud_file,
                max_words=args.max_words,
                width=args.wordcloud_width,
                height=args.wordcloud_height
            ):
                print(f"\n✅ 词云已生成: {args.wordcloud_file}")
            else:
                print("\n❌ 词云生成失败")
        
        # 下载论文
        if args.download:
            success_count = crawler.download_papers(
                all_papers, 
                download_dir=args.download_dir,
                max_downloads=args.max_downloads
            )
            print(f"\n下载完成: {success_count} 篇论文")
            
    except KeyboardInterrupt:
        logger.info("用户中断操作")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")


if __name__ == "__main__":
    main()