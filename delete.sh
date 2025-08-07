#!/bin/bash

set -e
export AWS_PAGER=""

APP_NAME="jewelry-app"
ENV_NAME="jewelry-env"
REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
ECR_URL="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$APP_NAME"
S3_BUCKET="jewelry-shop-s3-bucket"

echo "🛑 Terminating Elastic Beanstalk environment: $ENV_NAME"
aws elasticbeanstalk terminate-environment \
  --environment-name "$ENV_NAME" \
  --region "$REGION" || echo "Environment not found."

echo "⏳ Waiting for environment to terminate..."
aws elasticbeanstalk wait environment-terminated \
  --environment-names "$ENV_NAME" \
  --region "$REGION" || echo "Termination wait skipped."

echo "🧨 Deleting Elastic Beanstalk application: $APP_NAME"
aws elasticbeanstalk delete-application \
  --application-name "$APP_NAME" \
  --region "$REGION" \
  --terminate-env-by-force || echo "Application may already be gone."

echo "🗑️ Deleting Docker image from ECR..."
IMAGE_DIGEST=$(aws ecr list-images \
  --repository-name "$APP_NAME" \
  --region "$REGION" \
  --query 'imageIds[*].imageDigest' \
  --output text)

if [[ -n "$IMAGE_DIGEST" ]]; then
  aws ecr batch-delete-image \
    --repository-name "$APP_NAME" \
    --image-ids imageDigest="$IMAGE_DIGEST" \
    --region "$REGION"
fi

echo "🧹 Deleting ECR repository: $APP_NAME"
aws ecr delete-repository \
  --repository-name "$APP_NAME" \
  --region "$REGION" \
  --force || echo "ECR repo may already be gone."

echo "🧼 Deleting all contents in S3 bucket: $S3_BUCKET"
aws s3 rm s3://$S3_BUCKET --recursive --region "$REGION" || echo "No files found."

echo "🪣 Deleting the S3 bucket itself..."
aws s3api delete-bucket \
  --bucket "$S3_BUCKET" \
  --region "$REGION" || echo "S3 bucket may already be deleted."

echo "✅ All AWS resources deleted successfully."
