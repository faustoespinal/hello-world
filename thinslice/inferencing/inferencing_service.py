import requests
from common.helper import read_config
import json
from flask import jsonify

class InferencingService:
    workflow_manager_host = None

    def __init__(self):
        self.workflow_manager_host = read_config.get_workflow_manager_host()

    def run_inferencing_workflow(self, workflow_name, workflow_version, series_id, study_id):
        if self.workflow_manager_host is None:
            err = dict()
            err["message"] = "Workflow manager host not found"
            err["status_code"] = 500
            raise Exception(err)
        elif workflow_name is None or workflow_version is None:
            err = dict()
            err["message"] = "Please select workflow type"
            err["status_code"] = 500
            raise Exception(err)
        elif series_id is None or study_id is None:
            err = dict()
            err["message"] = "'Please select study and series before executing workflow'"
            err["status_code"] = 500
            raise Exception(err)

        api_endpoint = self.workflow_manager_host + "/api/workflow"
        payload = dict()
        payload["name"] = workflow_name
        payload["version"] = workflow_version
        payload["input"] = dict()
        payload["input"]["series"] = series_id
        payload["input"]["study"] = study_id

        json_payload = json.dumps(payload)
        print(json_payload)
        response_received = requests.post(api_endpoint, json=json.loads(json_payload))
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)
        print(response_received.text)
        result = dict()
        result["workflow_id"] = response_received.text
        return result

    def get_workflow_status(self, workflow_id):
        if self.workflow_manager_host is None:
            err = dict()
            err["message"] = "Workflow manager host not found"
            err["status_code"] = 500
            raise Exception(err)

        api_endpoint = self.workflow_manager_host + "/api/workflow/" + workflow_id
        response_received = requests.get(api_endpoint)
        print(response_received.status_code)
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

    def get_all_active_workflow(self):
        if self.workflow_manager_host is None:
            err = dict()
            err["message"] = "Workflow manager host not found"
            err["status_code"] = 500
            raise Exception(err)

        api_endpoint = self.workflow_manager_host + "/api/workflow/search/"
        response_received = requests.get(api_endpoint)

        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)

        json_response = response_received.json()
        result = list()
        for workflow in json_response["results"]:
            if workflow["status"] == "RUNNING":
                temp = dict()
                temp["workflow_name"] = workflow["workflowType"]
                temp["workflow_version"] = workflow["version"]
                temp["workflow_id"] = workflow["workflowId"]
                result.append(temp)
        print(response_received.status_code)
        print(response_received.text)
        return result

    def terminate_workflow(self, workflow_id_array):
        if self.workflow_manager_host is None:
            err = dict()
            err["message"] = "Workflow manager host not found"
            err["status_code"] = 500
            raise Exception(err)
        result = list()
        for workflow_id in workflow_id_array:
            print(workflow_id)
            api_endpoint = self.workflow_manager_host + "/api/workflow/" + workflow_id
            response_received = requests.delete(api_endpoint)

            if response_received.status_code != 204:
                err = dict()
                err["message"] = response_received.text
                err["status_code"] = response_received.status_code
                raise Exception(err)
        temp = dict()
        temp["status"] = workflow_id + " terminated"
        temp["status_code"] = response_received.status_code
        result.append(temp)
        return result


# if __name__ == '__main__':
#     Is = InferencingService()
#     print(Is.get_workflow_status("d61ca378-b59c-4be2-adc8-0b4e7172cb47"))
#     print(Is.get_all_active_workflow())
#     print(Is.terminate_workflow("d25d5043-78a4-40e9-be29-6c26c9368dfb"))
#     print(Is.run_inferencing_workflow("ptx_workflow", 1, "1.3.6.1.4.1.19291.2.1.2.240241528817129608497745535",
#                                       "1.2.276.0.7238010.5.1.2.0.79867.1586805178.13"))
