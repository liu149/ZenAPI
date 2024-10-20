from google.cloud import pubsub_v1
import time

# 设置您的 Google Cloud 项目 ID、主题名称和订阅名称
project_id = "bamboo-zephyr-435715-f7"
subscription_id = "test-topic-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}")

try:
    streaming_pull_future.result(timeout=30)
except TimeoutError:
    streaming_pull_future.cancel()
    print("Streaming pull future canceled.")
