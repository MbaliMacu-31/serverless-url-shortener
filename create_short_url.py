import json
import random
import string
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'UrlShortener'))

# Base URL where your redirect endpoint lives (set this after deploying API Gateway)
BASE_URL = os.environ.get('BASE_URL', 'https://your-api-id.execute-api.your-region.amazonaws.com/prod')


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('url')

        if not long_url:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing "url" in request body'})
            }

        # Generate a short code, retry on the rare collision
        short_code = generate_short_code()
        attempts = 0
        while attempts < 5:
            existing = table.get_item(Key={'shortCode': short_code})
            if 'Item' not in existing:
                break
            short_code = generate_short_code()
            attempts += 1

        table.put_item(Item={
            'shortCode': short_code,
            'longUrl': long_url
        })

        short_url = f"{BASE_URL}/{short_code}"

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'shortUrl': short_url, 'shortCode': short_code})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
