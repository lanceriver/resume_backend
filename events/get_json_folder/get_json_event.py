import sys
import json
import os

def load_json_event(file_name):
    PATH = os.path.join(os.path.dirname(__file__), file_name)
    json_event = open(PATH, "r")
    return json_event