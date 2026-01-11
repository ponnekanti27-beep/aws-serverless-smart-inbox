#!/bin/bash

# Load environment variables
set -a  # Automatically export variables
source .env
set +a

echo "🧹 Cleaning up AWS Smart Inbox resources..."
echo "📦 Account: 684124087486"
echo "🌎 Region: $REGION"
echo ""

# Delete S3 buckets (WARNING: DELETES ALL DATA)
echo "🗑️  Deleting S3 buckets..."
aws s3 rb "s3://$BUCKET_NAME" --force || echo "⚠️  Bucket $BUCKET_NAME already deleted or error"
aws s3 rb "s3://$PROCESSED_BUCKET" --force || echo "⚠️  Bucket $PROCESSED_BUCKET already deleted or error"
echo ""

# Delete SQS queues
echo "📬 Deleting SQS queues..."
aws sqs delete-queue --queue-url "$HIGH_PRIORITY_URL" || echo "⚠️  High priority queue already deleted"
aws sqs delete-queue --queue-url "$NORMAL_PRIORITY_URL" || echo "⚠️  Normal priority queue already deleted"
echo ""

# Delete Lambda function (adjust name if different)
echo "⚡ Deleting Lambda function..."
aws lambda delete-function --function-name smart-inbox-sentiment-analyzer --region "$REGION" || echo "⚠️  Lambda function already deleted or different name"
echo ""

# Delete IAM role and policy (be careful - may affect other resources)
echo "🔐 Deleting IAM role (WARNING: may affect other Lambdas)..."
aws iam detach-role-policy --role-name "SmartInboxLambdaRole" --policy-arn "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole" || true
aws iam delete-role-policy --role-name "SmartInboxLambdaRole" --policy-name "SmartInboxPolicy" || true
aws iam delete-role --role-name "SmartInboxLambdaRole" || echo "⚠️  IAM role already deleted or protected"
echo ""

echo "✅ Cleanup complete!"
echo "💰 Check AWS Billing Dashboard to confirm no charges."


