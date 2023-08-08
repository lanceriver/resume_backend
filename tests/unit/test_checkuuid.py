import json
import pytest
import uuid
import random
import sys
import os



os.environ["TABLE_NAME"] = "mock_uuid"

from resume_backend.lambdas.checkUUID import app

def init_list(mock_data):
    response = mock_data.scan()
    sample_uuid_list = response["Items"]
    return sample_uuid_list

def test_unique_uuid(mock_data):
    sample_uuid = str(uuid.uuid4())
    uuid_json = {
        "body":{"uuid":sample_uuid}
    }
    json_string = json.dumps(uuid_json)
    print(json_string)
    response = app.lambda_handler(json_string,"")
    result = response['body']
    assert result == "false", "uuid is NOT unique when it should be unique"

def test_same_uuid(mock_data):
    random_num = random.randint(0,9)
    sample_uuid_list = init_list(mock_data)
    sample_uuid = sample_uuid_list[random_num]['uuid']
    uuid_json = {
        "body":{"uuid":sample_uuid}
    }
    json_string = json.dumps(uuid_json)
    response = app.lambda_handler(json_string,"")
    result = response['body']
    assert result == "true", "uuid is unique when it should be the same"  