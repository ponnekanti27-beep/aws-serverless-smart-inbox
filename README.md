cat > README.md <<'EOF'
# AWS Smart Inbox Sentiment Analyzer

A serverless application that automatically analyzes message sentiment and routes them to priority queues.

## Architecture
```
[S3 Upload] → [Lambda Function] → [AWS Comprehend] → [SQS Queues]
                                                      ├─ High Priority (Negative)
                                                      └─ Normal Priority (Positive/Neutral)
```

## Features

- 📧 Automatic message ingestion via S3
- 🧠 Real-time sentiment analysis using AWS Comprehend
- 🚦 Smart routing based on negative sentiment threshold (>0.5)
- 💾 Processed message storage with metadata
- 📊 Separate queues for priority handling

## Cost Estimate

- S3: ~$0.05/month (for 1000 messages)
- Lambda: ~$0.10/month
- Comprehend: ~$0.10/month
- SQS: Free tier covers most usage
- **Total: ~$0.20-$1/month**

## Testing

Upload a message:
```bash
aws s3 cp sample-messages/negative.txt s3://$BUCKET_NAME/incoming/test.txt
```

Monitor queues:
```bash
python3 monitor_queues.py
```

## Project Structure
```
aws-smart-inbox-sentiment/
├── lambda/
│   └── sentiment-analyzer/
│       ├── lambda_function.py
│       └── requirements.txt
├── infrastructure/
│   ├── lambda-role-policy.json
│   ├── trust-policy.json
│   └── s3-notification.json
├── sample-messages/
│   ├── positive.txt
│   ├── negative.txt
│   ├── neutral.txt
│   └── mixed.txt
├── monitor_queues.py
├── .env
└── README.md
```

## Author

Built following Zero To Cloud's AWS ML project guide.
EOF
