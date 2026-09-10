import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'UrlShortener'))


def lambda_handler(event, context):
    try:
        # API Gateway path parameter, e.g. /abc123
        short_code = event.get('pathParameters', {}).get('shortCode')

        if not short_code:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing short code'})
            }

        result = table.get_item(Key={'shortCode': short_code})
        item = result.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Short URL not found'})
            }

        # 302 redirect to the original URL
        return {
            'statusCode': 302,
            'headers': {
                'Location': item['longUrl']
            },
            'body': ''
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
