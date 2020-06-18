import requests
from common.helper import read_config
import json
from flask import jsonify

class ProcessedImageService:
    def __init__(self):
        self.QIDO_URL = read_config.get_QIDO_host()

    def get_processed_image_studies(self):
        storeID = "EIS.DCM"
        api_endpoint = self.QIDO_URL + "/eis/v1/store/"+ storeID +"/studies/?includeField=00100020,00100010,00081030,00200010,00080020,00080060"
        response_received = requests.get(api_endpoint)
        print(response_received)
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)

        json_response = response_received.json()
        result = dict()
        result["status"] = json_response["status"]
        result["output"] = json_response["output"]["Output"]
        return result

    def get_processed_image_series(self, studyInstanceID):
        storeID = "EIS.DCM"
        api_endpoint = self.QIDO_URL + "/eis/v1/store/" + storeID +  "/studies/" + studyInstanceID +  "/series?includeField=0008103E,0020000E,00200011,00201209"
        print(response_received)
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)

        json_response = response_received.json()
        result = dict()
        result["status"] = json_response["status"]
        result["output"] = json_response["output"]["Output"]
        return result