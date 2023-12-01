import json
import requests

def lambda_handler(event, context):
    ngrok_url = "https://3472-104-222-28-177.ngrok-free.app"  # Replace with your ngrok URL
    data = {
        "bucket": event['Records'][0]['s3']['bucket']['name'],
        "key": event['Records'][0]['s3']['object']['key']
    }
    response = requests.post(ngrok_url, json=data)
    return {
        'statusCode': 200,
        'body': json.dumps('Webhook sent successfully.')
    }

