import json
import boto3
import os

table_name = os.getenv("TABLE_NAME", "website_userIDs")
dynamodb = boto3.resource('dynamodb')
uuid_table = dynamodb.Table(table_name)
def lambda_handler(event, context):
    # TODO implement
    if (isinstance(event, dict) == True):
        uuid_dict = json.loads(event['body'])
    else:
        uuid_event = json.loads(event)
        uuid_dict = uuid_event['body']
    uuid_table.put_item(
        Item={
            'uuid': uuid_dict['uuid']
        }
    )
    response = uuid_table.get_item(
        Key={
            'uuid': uuid_dict['uuid']
        }
    )
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps(response, default=str)
    }
