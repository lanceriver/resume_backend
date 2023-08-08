import pytest
import os
import moto
import boto3
import uuid
import json
from moto import mock_dynamodb, mock_apigateway

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture
def mock_db(aws_credentials):
    with mock_dynamodb():
        dynamodb = boto3.resource("dynamodb")
        yield dynamodb

@pytest.fixture
def create_mock_db(mock_db):
    with mock_dynamodb():
        mock_uuid_db = mock_db.create_table(
            TableName="mock_uuid",
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName':'uuid',
                    'AttributeType':'S'
            }
            ],
            ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
            }
        )
        return mock_uuid_db
    
@pytest.fixture
def create_mock_visitor_count(mock_db):
    with mock_dynamodb():
        mock_visitor_count_db = mock_db.create_table(
            TableName="mock_visitor_count",
            KeySchema=[
                {
                    'AttributeName': 'website_url',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName':'website_url',
                    'AttributeType':'S'
            }
            ],
            ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
            }
        )
        return mock_visitor_count_db
    
@pytest.fixture
def mock_data(create_mock_db):
    table = create_mock_db
    i = 0
    while (i < 10):
        mock_uuid = str(uuid.uuid4())
        table.put_item(
            Item={
                'uuid':mock_uuid
            }
        )
        i += 1
    return table

@pytest.fixture
def mock_visitor_count(create_mock_visitor_count):
    table = create_mock_visitor_count
    table.put_item(
        Item={
            'website_url':'https://lanceriver.com',
            'viewer_count':0
        }
    )
    return table

@pytest.fixture
def sample_uuid_json():
    sample_uuid = str(uuid.uuid4())
    uuid_json = {
        "body":{"uuid":sample_uuid}
    }
    json_string = json.dumps(uuid_json)
    return json_string

