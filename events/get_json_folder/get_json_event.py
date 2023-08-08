import sys
import json
import os

PATH = os.path.join(os.path.dirname(__file__), 'get_event.json')

def load_json_event():
    json_event = open(PATH, "r")
    return json_event