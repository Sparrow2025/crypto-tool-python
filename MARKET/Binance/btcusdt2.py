from binance.lib.utils import config_logging
import logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient
import psycopg2
import json
import os

# 连接PostgreSQL数据库
conn = psycopg2.connect("dbname=trader user=postgres password=makemoney@123")
cur = conn.cursor()

# 创建表格（如果尚未创建）
cur.execute("""
CREATE TABLE IF NOT EXISTS agg_trades (
    event_type VARCHAR(50),
    event_time BIGINT,
    symbol VARCHAR(20),
    aggregate_trade_id BIGINT,
    price DECIMAL(18, 8),
    quantity DECIMAL(18, 8),
    first_trade_id BIGINT,
    last_trade_id BIGINT,
    trade_time BIGINT,
    active_direction SMALLINT
);
""")
conn.commit()


# 定义回调函数
def on_message(message):
    data = json.loads(message)
    # 提取所需字段并插入到数据库
    cur.execute("""
        INSERT INTO agg_trades (event_type, event_time, symbol, aggregate_trade_id, price, quantity, 
                                 first_trade_id, last_trade_id, trade_time, active_direction)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['e'],
        data['E'],
        data['s'],
        data['a'],
        data['p'],
        data['q'],
        data['f'],
        data['l'],
        data['T'],
        1 if data['m'] else 0  # 1代表主动卖出，0代表主动买入
    ))
    conn.commit()


def on_ping(ws, message):
    # 使用ws.pong()回应ping消息
    ws.pong(message)  # 假设message是ping的payload


def set_proxy():
    # 设置代理
    os.environ['HTTPS_PROXY'] = 'https://127.0.0.1:7890'
    os.environ['HTTP_PROXY'] = 'https://127.0.0.1:7890'


def unset_proxy():
    # 取消代理
    os.environ.pop('HTTPS_PROXY')
    os.environ.pop('HTTP_PROXY')


def message_handler(_, message):
    logging.info(message)


if __name__ == '__main__':
    try:
        set_proxy()
        # 创建Futures对象
        client = UMFuturesWebsocketClient(on_message=message_handler, is_combined=True)
        # 连接到WebSocket并监听实时交易数据
        client.agg_trade(symbol='btcusdt', callback=on_message)
    finally:
        unset_proxy()
