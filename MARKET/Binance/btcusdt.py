import websocket
import json
import psycopg2
import os

# 连接PostgreSQL数据库
conn = psycopg2.connect("dbname=trader user=postgres password=makemoney@123")
cur = conn.cursor()


def on_message(ws, message):
    data = json.loads(message)
    print(data)
    # 提取所需字段
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
        1 if data['m'] else 0  # 0代表买方，1代表卖方
    ))
    conn.commit()


def on_ping(ws, message):
    print("ping, msg=", message)
    ws.send(message, opcode= 0xA)  # 回复pong消息


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")
    cur.close()
    conn.close()


def on_open(ws):
    print("### opened ###")

def set_proxy():
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'

def unset_proxy():
    os.environ.pop('HTTPS_PROXY')
    os.environ.pop('HTTP_PROXY')

if __name__ == "__main__":
    try:
        set_proxy()
        # 设置代理
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://fstream.binance.com/ws/btcusdt@aggTrade",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
        ws.on_open = on_open
        ws.on_ping = on_ping
        ws.run_forever()
        cur.close()
        conn.close()
    finally:
        unset_proxy()

