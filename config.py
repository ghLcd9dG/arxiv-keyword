"""
arXiv 爬虫配置文件
"""

# 默认配置
DEFAULT_CONFIG = {
    # 基础设置
    'base_url': 'https://arxiv.org',
    'delay': 1.0,  # 请求间隔时间（秒）
    'timeout': 30,  # 请求超时时间（秒）
    
    # 爬取设置
    'max_papers': 50,  # 默认最大论文数量
    'items_per_page': 50,  # 每页论文数量
    'start_page': 0,  # 起始页码
    
    # 下载设置
    'download_dir': 'papers',  # 默认下载目录
    'max_downloads': None,  # 最大下载数量（None表示无限制）
    'download_timeout': 60,  # 下载超时时间（秒）
    
    # 关键词提取设置
    'top_keywords': 20,  # 默认提取关键词数量
    'min_word_length': 3,  # 最小词长
    
    # 停用词列表
    'stop_words': {
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
        'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
    },
    
    # 常用栏目代码
    'categories': {
        'cs.AI': '人工智能',
        'cs.CV': '计算机视觉', 
        'cs.LG': '机器学习',
        'cs.CL': '计算语言学',
        'cs.NE': '神经网络与进化计算',
        'cs.RO': '机器人学',
        'cs.SE': '软件工程',
        'cs.IR': '信息检索',
        'cs.CC': '计算复杂性',
        'cs.DS': '数据结构与算法',
        'math.ST': '统计学',
        'stat.ML': '机器学习统计',
        'q-bio.QM': '定量生物学',
        'physics.bio-ph': '生物物理学'
    },
    
    # 日志设置
    'log_level': 'INFO',
    'log_format': '%(asctime)s - %(levelname)s - %(message)s',
    
    # 输出设置
    'output_format': 'json',  # 输出格式：json, csv, txt
    'save_papers_info': True,  # 是否保存论文信息
    'papers_info_filename': 'papers_info.json',  # 论文信息文件名
}

# 用户自定义配置（可以覆盖默认配置）
USER_CONFIG = {
    # 在这里添加你的自定义配置
    # 'delay': 2.0,  # 增加请求间隔
    # 'max_papers': 100,  # 增加论文数量
    # 'download_dir': 'my_papers',  # 自定义下载目录
}

def get_config():
    """获取合并后的配置"""
    config = DEFAULT_CONFIG.copy()
    config.update(USER_CONFIG)
    return config

def get_category_name(category_code):
    """根据栏目代码获取中文名称"""
    config = get_config()
    return config['categories'].get(category_code, category_code)

def get_stop_words():
    """获取停用词列表"""
    config = get_config()
    return config['stop_words']

def get_common_categories():
    """获取常用栏目列表"""
    config = get_config()
    return list(config['categories'].keys())