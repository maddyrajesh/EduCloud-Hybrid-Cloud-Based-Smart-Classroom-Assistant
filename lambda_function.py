import json
import requests

def lambda_handler(event, context):
    if 'Records' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps('No S3 event data found.')
        }

    ngrok_url = "https://f5e5-104-222-28-177.ngrok-free.app/webhook"  # Replace with your ngrok URL
    data = {
        "bucket": event['Records'][0]['s3']['bucket']['name'],
        "key": event['Records'][0]['s3']['object']['key']
    }
    response = requests.post(ngrok_url, json=data)
    return {
        'statusCode': 200,
        'body': json.dumps('Webhook sent successfully.')
    }
