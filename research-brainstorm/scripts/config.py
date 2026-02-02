"""
配置文件
用于管理 API 密钥和其他设置
"""

import os

# PubMed API 配置
# 从环境变量读取 API Key
# 获取免费 API Key: https://www.ncbi.nlm.nih.gov/account/
PUBMED_API_KEY = os.environ.get("PUBMED_API_KEY", "")

# 检索设置
DEFAULT_MAX_RESULTS = 20  # 默认返回最大结果数
REQUEST_TIMEOUT = 30  # 请求超时时间（秒）

# 新颖性判断阈值
NOVELTY_THRESHOLDS = {
    "red_count": 10,      # 超过此数量为红灯
    "recent_years": 2,    # 近期文献的定义（年）
}

# 输出设置
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)
