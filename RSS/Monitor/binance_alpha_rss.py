import sys
import time
import feedparser
import requests
import hashlib
import os

from numpy.core.defchararray import title

# 配置项
RSS_URLS = [
    "https://rss.panewslab.com/zh/tvsq/rss"
]
BARK_API = "https://api.day.app/device_id/标题/Binance-Alpha-积分-监控"

# 和 BARK——API一样从环境变量中获取
STORAGE_FILE = "processed_entries.txt"


# 去重存储
def load_processed_entries():
    if not os.path.exists(STORAGE_FILE):
        return set()
    with open(STORAGE_FILE, 'r') as f:
        return set(f.read().splitlines())


def save_entry(entry_id):
    with open(STORAGE_FILE, 'a') as f:
        f.write(f"{entry_id}\n")


# 处理RSS更新
def check_rss():
    processed = load_processed_entries()
    for url in RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            entry_id = hashlib.md5(entry.link.encode()).hexdigest()  # 生成唯一ID
            if entry_id not in processed:
                # 信息处理（示例：提取标题+链接）
                title = entry.title
                # description = entry.description
                # link = entry.link
                # message = f"{title}\n{link}"
                # 推送至Bark
                process_data(title, description=entry.description if 'description' in entry else None)
                save_entry(entry_id)


def process_data(data, description=None):
    # 预定义的规则条件
    required_keywords = ['Binance', 'Alpha', '积分']  # 需要包含的关键词列表
    # 规则1：标题必须包含任意一个关键词
    title_condition = any(keyword.lower() in data.lower() for keyword in required_keywords)

    # 规则2：附加其他条件（示例）
    # content_condition = len(content) > 10
    if title_condition:
        send_notification(data, description)  # 你的推送函数

def send_notification(title, description=None):
    # 推送至Bark
    # description 中有html标签，需要去掉
    bark_url = f"{BARK_API.replace('标题', title).replace('Binance-Alpha-积分-监控', description.replace('<p>', '').replace('</p>', '') if description else '')}"
    requests.get(bark_url)
    # 发送推送通知

if __name__ == "__main__":
    # 从环境变量取 device_id
    device_id = os.getenv('BARK_DEVICE_ID')
    store_pre = os.getenv('BARK_MONITOR_BINANCE_ALPHA')
    BARK_API = BARK_API.replace('device_id', device_id) if device_id else BARK_API
    STORAGE_FILE = store_pre + "/" + STORAGE_FILE
    while True:
        check_rss()
        time.sleep(300)  # 每5分钟检查一次
