import json
import boto3

dynamodb = boto3.resource('dynamodb')
visitor_table = dynamodb.Table('lancerivervisitor_counter')
def lambda_handler(event, context):
    # TODO implement
    
    response = visitor_table.update_item(
        Key={"website_url": "https://lanceriver.com"},
        UpdateExpression="set viewer_count = viewer_count + :n",
        ExpressionAttributeValues={
            ":n": 1,
        },
        ReturnValues="UPDATED_NEW"
        )
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin":"*",
        },
        'body': json.dumps(response,default=str)
    }
