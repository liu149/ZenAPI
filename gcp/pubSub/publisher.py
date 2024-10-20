from google.cloud import pubsub_v1
import os

# 设置您的 Google Cloud 项目 ID 和主题名称
project_id = "bamboo-zephyr-435715-f7"
topic_id = "test-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_message(message):
    data = message.encode("utf-8")
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    # message = input("Enter a message to publish: ")
    publish_message("Hello")
