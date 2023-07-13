import json
import boto3

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Allow-Access-Control-Origin' : '*'
        },
        'body': json.dumps(event, default=str),
    }