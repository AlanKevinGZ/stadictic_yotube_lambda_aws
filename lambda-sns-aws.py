
# ===============================

 # Lambda function to send an email notification when a new file is generated in S3
 # Create  environment variable in AWS Lambda:
 # TOPIC_ARN = "your-sns-topic-arn"
 
 # AUTHOR: https://github.com/AlanKevinGZ 2026

# ===============================

import os
import urllib.parse

import boto3

sns = boto3.client("sns")

TOPIC_ARN = os.environ["TOPIC_ARN"]


def lambda_handler(event, context):

    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"]
    )

    message = f"""YouTube ETL Pipeline - SUCCESS

El pipeline se ejecutó correctamente y se detectó un nuevo archivo en Amazon S3.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 Bucket
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{bucket}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Archivo generado
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{key}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 Estado
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUCCESS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙ Servicio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AWS Lambda → Amazon S3 → Amazon SNS

Este correo fue generado automáticamente.
"""

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="YouTube ETL Pipeline - SUCCESS",
        Message=message
    )

    return {
        "statusCode": 200,
        "body": "Correo enviado."
    }