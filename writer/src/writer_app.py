import json
import logging
import os
import signal
import threading
import random

from kafka import KafkaConsumer
from sqlalchemy import text
from database import get_db

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SHARD_IDS = [0, 1]

# Kafka configuration
KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
KAFKA_PORT = os.getenv("KAFKA_PORT", "9092")
KAFKA_BROKER_URL = f"{KAFKA_HOST}:{KAFKA_PORT}"

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "event_server")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")

# Kafka Consumer Setup using kafka-python
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER_URL,
    group_id=KAFKA_GROUP_ID,
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)


def determine_shard_id_for_new_user():
    # Uniform distribution for each shard
    return random.choice(SHARD_IDS)


def shutdown(signal, frame):
    print("Shutting down consumer...")
    consumer.close()
    exit(0)


def start_consumer():
    while True:
        for msg in consumer:
            user_data = msg.value
            # Insert user_data into the database
            db = next(get_db())

            try:
                shard_id = determine_shard_id_for_new_user()
                insert_query = f"INSERT INTO users (login, first_name, last_name, email) VALUES ('{user_data['login']}', '{user_data['first_name']}', '{user_data['last_name']}', '{user_data['email']}') RETURNING *  -- sharding:{shard_id}"

                new_user = db.execute(text(insert_query)).fetchone()
                db.commit()  # Commit the transaction

                logger.info(f"Inserted: {json.dumps(user_data)} into {shard_id}")
            except Exception as e:
                logger.error(f"Error inserting user data: {e}")
                db.rollback()
            finally:
                db.close()

            consumer.commit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    threading.Thread(target=start_consumer).start()
