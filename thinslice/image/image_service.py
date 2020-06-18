import requests
# from .common.helper import read_config
import json
from flask import jsonify


class ImageService:
    def __init__(self):
        # self.QIDO_URL = read_config.get_QIDO_host()
        self.QIDO_URL = 'http://10.12.40.157:30043'
        self.DICOM_DICTIONARY = {

            'patient_id': "00100020",
            'patient_name': "00100010",

            'study_description': "00081030",
            'study_instance_uid': "0020000D",
            'study_uid': "00200010",
            'study_date': "00080020",

            'series_description': "0008103E",
            'series_instance_uid': "0020000E",
            'series_number': "00200011",

            'number_of_series_related_instances': "00201209"
        }
        self.selected_studied_uid = ''

    def get_image_studies(self):
        storeID = "EIS.DCM"
        api_endpoint = self.QIDO_URL + "/eis/v1/store/" + storeID + \
            "/studies/?includeField=00100020,00100010,00081030,00200010,00080020,00080060"
        response_received = requests.get(api_endpoint)
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)

        json_response = response_received.json()
        if len(json_response) > 0:
            self.selected_studied_uid = json_response[0][self.DICOM_DICTIONARY['study_instance_uid']]['Value'][0]
            print(self.selected_studied_uid)
        return json_response

    def get_image_series(self, studyInstanceID):
        storeID = "EIS.DCM"
        print("lol")
        api_endpoint = self.QIDO_URL + "/eis/v1/store/" + storeID + "/studies/" + \
            studyInstanceID + "/series?includeField=0008103E,0020000E,00200011,00201209"
        response_received = requests.get(api_endpoint)
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)

        json_response = response_received.json()
        return json_response

