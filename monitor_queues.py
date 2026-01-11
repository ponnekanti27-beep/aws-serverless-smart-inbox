import boto3
import json
import os
from datetime import datetime

# Load environment variables from .env file (create this first)
try:
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value
except FileNotFoundError:
    print("Create .env file first!")

sqs = boto3.client('sqs')

HIGH_PRIORITY_URL = os.environ.get('HIGH_PRIORITY_URL')
NORMAL_PRIORITY_URL = os.environ.get('NORMAL_PRIORITY_URL')

def check_queue(queue_url, queue_name):
    print(f"\n{'='*60}")
    print(f"{queue_name} QUEUE")
    print('='*60)
    
    try:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            MessageAttributeNames=['All']
        )
        
        messages = response.get('Messages', [])
        
        if not messages:
            print("  ✅ No messages in queue")
            return
        
        print(f"  📨 Found {len(messages)} messages:")
        for i, msg in enumerate(messages, 1):
            body = json.loads(msg['Body'])
            print(f"\n    📄 Message {i}:")
            print(f"       File: {body.get('original_key', 'N/A')}")
            print(f"       Sentiment: {body.get('sentiment', 'N/A')}")
            print(f"       Negative: {body.get('negative_score', 0):.2f}")
            print(f"       Preview: {body.get('message', '')[:100]}...")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

if __name__ == '__main__':
    print("\n🔍 AWS SMART INBOX - QUEUE MONITOR")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if HIGH_PRIORITY_URL and NORMAL_PRIORITY_URL:
        check_queue(HIGH_PRIORITY_URL, "HIGH PRIORITY")
        check_queue(NORMAL_PRIORITY_URL, "NORMAL PRIORITY")
    else:
        print("❌ Set HIGH_PRIORITY_URL and NORMAL_PRIORITY_URL in .env")
    
    print("\n" + "="*60 + "\n")

