import json
import pytest
import uuid
import sys
import os

sys.path.insert(0, "/Users/lance/Downloads/resume_backend/lambdas")

os.environ["TABLE_NAME"] = "mock_uuid"

from storeUUID import app

def test_store_valid_uuid(sample_uuid_json, mock_data):
    result = json.loads(sample_uuid_json)
    expected_result = result["body"]["uuid"]
    response = app.lambda_handler(sample_uuid_json,"")
    parsed_response = json.loads(response["body"])
    actual_response = parsed_response["Item"]["uuid"]
    assert actual_response == expected_result, "uuid not saved successfully!"
