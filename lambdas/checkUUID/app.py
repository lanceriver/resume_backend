import json
import boto3
import os

table_name = os.getenv("TABLE_NAME", "website_userIDs")
dynamodb = boto3.resource('dynamodb')
uuid_table = dynamodb.Table(table_name)


def cookie_unique(uuid):
    response = uuid_table.scan()
    items = response['Items']
    for value in range(len(items)):
        if uuid == items[value]['uuid']:
            return True
        else: continue
    return False

def lambda_handler(event, context):
    if (isinstance(event, dict) == True):
        uuid_dict = json.loads(event['body'])
        uuid = uuid_dict['uuid']
    else:
        uuid_dict = json.loads(event)
        uuid = uuid_dict['body']['uuid']
    response = cookie_unique(uuid)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*"
        },
        'body': json.dumps(response, default=str)
    }

