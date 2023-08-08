import json
import pytest
import uuid
import sys
import os



os.environ["TABLE_NAME"] = "mock_visitor_count"
from resume_backend.lambdas.update_visitor_count import app

@pytest.fixture
def update_event(mock_visitor_count):
    json_test = open("/Users/lance/Downloads/resume_backend/events/event.json", "r")
    response = app.lambda_handler(json_test,"")
    response_body = json.loads(response['body'])
    viewer_count = int(response_body['Attributes']['viewer_count'])
    return viewer_count

def test_count_is_incrementing(update_event):
    initial_count = update_event
    json_test = open("/Users/lance/Downloads/resume_backend/events/event.json", "r")
    response = app.lambda_handler(json_test,"")
    response_body = json.loads(response['body'])
    viewer_count = int(response_body['Attributes']['viewer_count'])
    assert viewer_count == initial_count + 1
