import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')
sqs = boto3.client('sqs')

HIGH_PRIORITY_QUEUE = os.environ['HIGH_PRIORITY_QUEUE_URL']
NORMAL_PRIORITY_QUEUE = os.environ['NORMAL_PRIORITY_QUEUE_URL']
PROCESSED_BUCKET = os.environ['PROCESSED_BUCKET']

def lambda_handler(event, context):
    """
    Triggered by S3 upload. Analyzes sentiment and routes to appropriate queue.
    """
    
    for record in event['Records']:
        # Get the uploaded file details
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Processing: {bucket}/{key}")
        
        try:
            # Read message from S3
            response = s3.get_object(Bucket=bucket, Key=key)
            message_text = response['Body'].read().decode('utf-8')
            
            # Analyze sentiment
            sentiment_response = comprehend.detect_sentiment(
                Text=message_text,
                LanguageCode='en'
            )
            
            sentiment = sentiment_response['Sentiment']
            scores = sentiment_response['SentimentScore']
            
            # Determine priority based on negative sentiment
            negative_score = scores['Negative']
            is_high_priority = negative_score > 0.5  # Threshold for high priority
            
            # Prepare message metadata
            message_data = {
                'original_key': key,
                'message': message_text,
                'sentiment': sentiment,
                'scores': scores,
                'negative_score': negative_score,
                'timestamp': datetime.utcnow().isoformat(),
                'priority': 'HIGH' if is_high_priority else 'NORMAL'
            }
            
            # Route to appropriate queue
            queue_url = HIGH_PRIORITY_QUEUE if is_high_priority else NORMAL_PRIORITY_QUEUE
            
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(message_data),
                MessageAttributes={
                    'Sentiment': {'StringValue': sentiment, 'DataType': 'String'},
                    'NegativeScore': {'StringValue': str(negative_score), 'DataType': 'Number'}
                }
            )
            
            # Save processed message to processed bucket
            processed_key = f"processed/{key.split('/')[-1]}"
            s3.put_object(
                Bucket=PROCESSED_BUCKET,
                Key=processed_key,
                Body=json.dumps(message_data, indent=2),
                ContentType='application/json'
            )
            
            print(f"✓ Routed to {message_data['priority']} priority queue")
            print(f"  Sentiment: {sentiment} (Negative: {negative_score:.2f})")
            
        except Exception as e:
            print(f"✗ Error processing {key}: {str(e)}")
            raise
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
