import requests
from common.helper import read_config
import json
from flask import jsonify

class EngineService:
    def __init__(self):
        self.EAI_IS = read_config.get_EAI_IS_host()

    def get_engine_status(self):
        api_endpoint = self.EAI_IS + "/ping"
        response_received = requests.get(api_endpoint)
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)
        result = dict()
        result["status"] = response_received.status_code
        return result

    def get_engine_model_list(self):
        api_endpoint = self.EAI_IS + "/list-models"
        response_received = requests.get(api_endpoint)
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)
        json_response = response_received.json()
        result = dict()
        result["status"] = response_received.status_code
        result["text"] = json_response
        return result

if __name__ == '__main__':
    engineService = EngineService()
    engineService.get_engine_status()
    engineService.get_engine_model_list() 