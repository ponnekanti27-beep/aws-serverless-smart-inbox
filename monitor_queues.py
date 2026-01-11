import boto3
import json
import os

# Load environment
env_vars = {}
with open('.env') as f:
    for line in f:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            env_vars[key] = value

sqs = boto3.client('sqs', region_name=env_vars['REGION'])

HIGH_PRIORITY_URL = env_vars['HIGH_PRIORITY_URL']
NORMAL_PRIORITY_URL = env_vars['NORMAL_PRIORITY_URL']

def check_queue(queue_url, queue_name):
    print(f"\n{'='*60}")
    print(f"{queue_name} QUEUE")
    print('='*60)
    
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        MessageAttributeNames=['All']
    )
    
    messages = response.get('Messages', [])
    
    if not messages:
        print("  No messages in queue")
        return
    
    for i, msg in enumerate(messages, 1):
        body = json.loads(msg['Body'])
        print(f"\n  Message {i}:")
        print(f"    File: {body['original_key']}")
        print(f"    Sentiment: {body['sentiment']}")
        print(f"    Negative Score: {body['negative_score']:.2f}")
        print(f"    Preview: {body['message'][:100]}...")

if __name__ == '__main__':
    from datetime import datetime
    print("\n🔍 AWS SMART INBOX - QUEUE MONITOR")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    check_queue(HIGH_PRIORITY_URL, "HIGH PRIORITY")
    check_queue(NORMAL_PRIORITY_URL, "NORMAL PRIORITY")
    
    print("\n" + "="*60 + "\n")
