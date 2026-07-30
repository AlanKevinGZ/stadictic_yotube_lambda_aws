
# ===============================

 # Lambda function to get YouTube channel statistics and save them to S3
 # Create  environment variable in AWS Lambda:
 # BUCKET_DESTINY = "your-input-bucket-name"
 # BUCKET_OUTPUT = "your-output-bucket-name"
 # API_KEY = "your-youtube-api-key"
 # FILE_CHANNELS = "channels.json"

 # AUTHOR: https://github.com/AlanKevinGZ 2026

# ===============================

import json
import os
from datetime import datetime
from io import StringIO

import boto3
import pandas as pd
import requests

s3_client = boto3.client("s3")


def get_stats(api_key, channel_id):
    url = (
        "https://youtube.googleapis.com/youtube/v3/channels"
        f"?part=snippet,statistics&id={channel_id}&key={api_key}"
    )

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    if not data.get("items"):
        raise Exception(f"No se encontró el canal: {channel_id}")

    item = data["items"][0]
    stats = item["statistics"]

    return {
        "Channel_id": channel_id,
        "Created_at": datetime.now().strftime("%Y-%m-%d"),
        "Channel_name": item["snippet"]["title"],
        "Total_Views": int(stats["viewCount"]),
        "Subscribers": int(stats["subscriberCount"]),
        "Video_count": int(stats["videoCount"])
    }


def channel_stats(channel_ids, api_key):
    data = []

    for channel_id in channel_ids:
        data.append(get_stats(api_key, channel_id))

    return pd.DataFrame(data)


def lambda_handler(event, context):

    input_bucket = os.environ["BUCKET_DESTINY"]
    output_bucket = os.environ["BUCKET_OUTPUT"]
    api_key = os.environ["API_KEY"]
    file_channels = os.environ["FILE_CHANNELS"]

    # Leer el archivo JSON desde S3
    response = s3_client.get_object(
        Bucket=input_bucket,
        Key=file_channels
    )

    channel_ids = json.loads(
        response["Body"].read().decode("utf-8")
    )

    if not channel_ids:
        raise ValueError("El archivo channels.json está vacío.")

    # Obtener estadísticas de los canales
    df_channels = channel_stats(channel_ids, api_key)

    # Convertir DataFrame a CSV en memoria
    csv_buffer = StringIO()
    df_channels.to_csv(csv_buffer, index=False)

    # Guardar CSV en el bucket de salida
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    s3_client.put_object(
        Bucket=output_bucket,
        Key=f'raw/youtube_stats_{timestamp}.csv',
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Proceso completado correctamente.")
    }