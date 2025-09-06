# arXiv 论文爬取和下载工具

这是一个用于从 arXiv 特定栏目爬取论文、提取关键词并下载PDF的工具。

## 功能特性

- 🚀 支持从任意 arXiv 栏目爬取论文
- 📄 自动分页获取大量论文
- 🔍 智能关键词提取
- ☁️ 生成词云图片
- 💾 批量下载PDF文件
- 📊 详细的进度显示和日志
- ⚙️ 可配置的请求间隔和重试机制

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 从 cs.AI 栏目获取最近50篇论文并提取关键词
python arxiv_crawler.py --category cs.AI --max-papers 50

# 获取论文并下载PDF文件
python arxiv_crawler.py --category cs.CV --max-papers 100 --download

# 从第2页开始获取论文
python arxiv_crawler.py --category cs.LG --max-papers 200 --start-page 1

# 生成词云图片
python arxiv_crawler.py --category cs.AI --max-papers 50 --wordcloud

# 生成自定义词云
python arxiv_crawler.py --category cs.AI --max-papers 50 --wordcloud --wordcloud-file ai_wordcloud.png --max-words 150
```

### 命令行参数

- `--category, -c`: arXiv 栏目代码，支持多个栏目（默认: cs.AI）
- `--max-papers, -n`: 最大论文数量（默认: 50）
- `--download, -d`: 是否下载PDF文件
- `--download-dir`: 下载目录（默认: papers）
- `--keywords, -k`: 提取关键词数量（默认: 20）
- `--delay`: 请求间隔时间（秒）（默认: 1.0）
- `--start-page`: 起始页码（默认: 0）
- `--wordcloud, -w`: 生成词云图片
- `--wordcloud-file`: 词云输出文件名（默认: wordcloud.png）
- `--max-words`: 词云最大词数（默认: 100）
- `--wordcloud-width`: 词云图片宽度（默认: 800）
- `--wordcloud-height`: 词云图片高度（默认: 400）

### 常用栏目代码

- `cs.AI`: Artificial Intelligence
- `cs.CV`: Computer Vision and Pattern Recognition
- `cs.CL`: Computation and Language
- `cs.LG`: Machine Learning
- `cs.NE`: Neural and Evolutionary Computing
- `cs.RO`: Robotics
- `math.ST`: Statistics Theory
- `stat.ML`: Machine Learning

## 输出文件

- `papers_info.json`: 论文详细信息
- `wordcloud.png`: 词云图片（如果启用）
- `papers/`: PDF文件下载目录
- 控制台输出关键词统计

## 示例

```bash
# 获取机器学习领域最近100篇论文，下载PDF并提取前30个关键词
python arxiv_crawler.py -c cs.LG -n 100 -d -k 30

# 从计算机视觉栏目获取大量论文（支持分页）
python arxiv_crawler.py -c cs.CV -n 500 -d --delay 0.5

# 生成词云并下载PDF
python arxiv_crawler.py -c cs.AI -n 100 -w -d

# 多栏目爬取
python arxiv_crawler.py --category cs.AI cs.CV cs.LG --max-papers 30

# 多栏目爬取并生成词云
python arxiv_crawler.py --category cs.AI cs.CV --max-papers 20 --wordcloud
```

## 注意事项

- 请遵守 arXiv 的使用条款，避免过于频繁的请求
- 建议设置适当的 `--delay` 参数（默认1秒）
- 大量下载时建议分批进行
- 程序会自动跳过已下载的文件

## 技术实现

- 使用 BeautifulSoup 解析HTML页面
- 支持分页获取大量论文
- 简单的词频统计进行关键词提取
- 可扩展的架构设计

## 扩展功能

可以进一步扩展的功能：
- 更智能的关键词提取（使用NLP库）
- 论文分类和标签
- 数据库存储
- Web界面
- 定时任务支持