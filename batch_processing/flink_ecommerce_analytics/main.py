import json
import time

from confluent_kafka import SerializingProducer
from datetime import datetime
from faker import Faker
import random


fake = Faker()


def generate_sales_transacions():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "productId": random.choice(
            ["product1", "product2", "product3", "product4", "product5", "product6"]
        ),
        "productName": random.choice(
            ["laptop", "mobile", "tablet", "watch", "headphone", "speaker"]
        ),
        "productCategory": random.choice(
            ["electronic", "fashion", "grocery", "home", "beauty", "sports"]
        ),
        "productPrice": round(random.uniform(10, 1000), 2),
        "productQuantity": random.randint(1, 10),
        "productBrand": random.choice(
            ["apple", "samsung", "oneplus", "mi", "boat", "sony"]
        ),
        "currency": random.choice(["USD", "GBP"]),
        "customerId": user["username"],
        "transactionDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        "paymentMethod": random.choice(
            ["credit_card", "debit_card", "online_transfer"]
        ),
    }


def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Messsge delivered: {msg.topic} [{msg.partiion()}]")


def main():
    topic = "financial_transactions"
    producer = SerializingProducer(
        {
            "bootstrap.servers": "localhost:9092",
        }
    )
    current_time = datetime.now()

    while (datetime.now() - current_time).seconds < 900:
        try:
            transaction = generate_sales_transacions()
            transaction["totalAmount"] = (
                transaction["productPrice"] * transaction["productQuantity"]
            )
            producer.produce(
                topic,
                key=transaction["transactionId"],
                value=json.dumps(transaction),
            )
            producer.poll(0)

            # Wait for 5 seconds before sending the next transaction mesage
            time.sleep(5)
            print("kafka Message got generated !")
        except BufferError:
            print("Buffer full! waiting....")
            time.sleep(1)
        except Exception as e:
            print(e)
            print("Error occurred")


if __name__ == "__main__":
    main()
