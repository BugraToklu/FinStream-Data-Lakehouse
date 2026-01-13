import time
import json
import random
import uuid
from kafka import KafkaProducer
from datetime import datetime


KAFKA_BOOTSTRAP_SERVERS = 'kafka:29092'
TOPIC_NAME = 'financial_trades'

TRADING_SYMBOLS = ["BTC-USD", "ETH-USD", "AAPL", "GOOGL", "TSLA", "AMZN"]
ORDER_TYPES = ["BUY", "SELL"]

def get_producer():
    print("Kafka Producer is starting...")
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

def generate_trade():
    symbol = random.choice(TRADING_SYMBOLS)
    price = round(random.uniform(100, 50000), 2)
    quantity = round(random.uniform(0.01, 10), 4)
    
    return {
        "trade_id": str(uuid.uuid4()),
        "symbol": symbol,
        "price": price,
        "quantity": quantity,
        "side": random.choice(ORDER_TYPES),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    producer = get_producer()
    print(f"Data flow has started -> Topic: {TOPIC_NAME}")
    
    try:
        while True:
            trade = generate_trade()
            producer.send(TOPIC_NAME, value=trade)
            print(f"Sent: {trade['symbol']} | ${trade['price']}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped.")