import json
import boto3
import os

table_name = os.getenv("TABLE_NAME", "lancerivervisitor_counter")
dynamodb = boto3.resource('dynamodb')
visitor_table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # TODO implement
    
    response = visitor_table.get_item(
        Key={
            'website_url': 'https://lanceriver.com'
        }
    )
    return {
        'statusCode' : 200,
        'headers': {
            "Access-Control-Allow-Origin":"*",
        },
        'body': json.dumps(response,default=str)
    }
