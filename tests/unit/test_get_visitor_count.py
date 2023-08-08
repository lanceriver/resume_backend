import json
import pytest
import sys
import os

sys.path.insert(0, "/Users/lance/Downloads/resume_backend/lambdas")
os.environ["TABLE_NAME"] = "mock_visitor_count"
from get_visitor_count import app

@pytest.fixture

def get_event(mock_visitor_count):
    json_event = open("/Users/lance/Downloads/resume_backend/events/get_event.json", "r")
    response = app.lambda_handler(json_event,"")
    response_body = json.loads(response['body'])
    viewer_count = int(response_body['Item']['viewer_count'])
    return viewer_count

def test_if_visitor_count_is_integer(get_event):
    assert type(get_event) is int, "Could not convert value to int!"

def test_if_visitor_count_is_positive(get_event):
    assert get_event >= 0, "Count is negative!"

def test_if_visitor_count_does_not_update_when_called_repeatedly(get_event):
    original_value = get_event
    i = 0
    while (i < 5):
        test_value = get_event
        assert test_value == original_value, "Not supposed to change!"
        i += 1