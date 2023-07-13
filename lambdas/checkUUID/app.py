import json
import boto3

dynamodb = boto3.resource('dynamodb')
uuid_table = dynamodb.Table('website_userIDs')

def cookie_unique(uuid):
    response = uuid_table.scan()
    items = response['Items']
    for value in range(len(items)):
        if uuid == items[value]['uuid']:
            return True
        else: continue
    return False

def lambda_handler(event, context):
    uuid_dict = json.loads(event['body'])
    uuid = uuid_dict['uuid']
    response = cookie_unique(uuid)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*"
        },
        'body': json.dumps(response, default=str)
    }

