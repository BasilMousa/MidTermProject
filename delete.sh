#!/bin/bash

# --- Configuration ---
APP_NAME="jewelry-app"
ENV_NAME="jewelry-env"
VERSION_LABEL="v1"
S3_BUCKET="your-s3-bucket-name"
ZIP_FILE="jewelry-dockerrun.zip"

# --- Confirm before proceeding ---
read -p "⚠️ This will DELETE the Elastic Beanstalk environment and application. Continue? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
    echo "Aborted."
    exit 1
fi

echo "⛔ Deleting Elastic Beanstalk environment: $ENV_NAME"
aws elasticbeanstalk terminate-environment --environment-name "$ENV_NAME"

echo "⌛ Waiting for environment termination..."
aws elasticbeanstalk wait environment-terminated --environment-name "$ENV_NAME"

echo "🧼 Deleting application version: $VERSION_LABEL"
aws elasticbeanstalk delete-application-version \
    --application-name "$APP_NAME" \
    --version-label "$VERSION_LABEL" \
    --delete-source-bundle

echo "🗑️ Deleting application: $APP_NAME"
aws elasticbeanstalk delete-application --application-name "$APP_NAME"

echo "🧹 Cleaning up ZIP file from S3: $ZIP_FILE"
aws s3 rm "s3://$S3_BUCKET/$ZIP_FILE"

echo "✅ Cleanup complete."
