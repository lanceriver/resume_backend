import json
import boto3

dynamodb = boto3.resource('dynamodb')
uuid_table = dynamodb.Table('website_userIDs')

def lambda_handler(event, context):
    # TODO implement
    uuid_dict = json.loads(event['body'])
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
