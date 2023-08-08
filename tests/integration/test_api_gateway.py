import os
import json
import uuid
import boto3
import pytest
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""

os.environ["AWS_SAM_STACK_NAME"] = "testingWebsiteStack"

sample_json = {
    "uuid": str(uuid.uuid4())
}

class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url_list(self):
        """ Get the API Gateway endpoint URLs from Cloudformation Stack outputs and output a list"""
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output["OutputValue"]for output in stack_outputs]

        if not api_outputs:
            raise KeyError(f"HelloWorldAPI not found in stack {stack_name}")

        return api_outputs # Extract url from stack outputs
    
    def test_get_uuid(self, api_gateway_url_list):
        """ Call the API Gateway endpoint and check the response """
        os.environ["TABLE_NAME"] = "test_user_id"
        url = extract_url("getUUID", api_gateway_url_list)
        response = requests.put(url, json=sample_json)
        assert response.status_code == 200
        assert response.json() == False
        
    def test_store_uuid(self, api_gateway_url_list):
        os.environ["TABLE_NAME"] = "test_user_id"
        url = extract_url("storeUUID", api_gateway_url_list)
        response = requests.put(url, json=sample_json)
        response_dict = response.json()
        response_body = response_dict["Item"]
        assert response.status_code == 200
        assert response_body == sample_json
    
    def test_get_visitor_count(self, api_gateway_url_list):
        os.environ["TABLE_NAME"] = "test_visitor_count"
        url = extract_url("get_visitor_count", api_gateway_url_list)
        response = requests.get(url)
        assert response.status_code == 200
        
    
    def test_update_visitor_count(self, api_gateway_url_list):
        os.environ["TABLE_NAME"] = "test_visitor_count"
        get_visitor_response = requests.get(extract_url("get_visitor_count", api_gateway_url_list))
        original_count = int(get_visitor_response.json()["Item"]["viewer_count"])
        url = extract_url("update_visitor_count", api_gateway_url_list)
        response = requests.put(url, "")
        print(response.json())
        final_count = int(response.json()["Attributes"]["viewer_count"])
        assert response.status_code == 200
        assert final_count == original_count + 1

def extract_url(path, api_gateway_url_list):
        for i in range(len(api_gateway_url_list)):
            if path in api_gateway_url_list[i]:
                return api_gateway_url_list[i]
        return