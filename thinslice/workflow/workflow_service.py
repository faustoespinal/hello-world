import requests
from common.helper import read_config


class WorkflowService:
    workflow_manager_host = None

    def __init__(self):
        self.workflow_manager_host = read_config.get_workflow_manager_host()

    def get_all_workflows(self):
        if self.workflow_manager_host is None:
            err = dict()
            err["message"] = "Workflow manager host not found"
            err["status_code"] = 500
            raise Exception(err)

        api_endpoint = self.workflow_manager_host + "/api/metadata/workflow"
        response_received = requests.get(api_endpoint)
        if response_received.status_code != 200:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)
        workflow_list = response_received.json()

        result = list()
        for i, workflow in enumerate(workflow_list):
            temp = dict()
            temp["workflow"] = workflow["name"]
            temp["version"] = workflow["version"]
            result.append(temp)
        return result

    def delete_workflow(self, workflow_name, workflow_version):
        if self.workflow_manager_host is None:
            err = dict()
            err["message"] = "Workflow manager host not found"
            err["status_code"] = 500
            raise Exception(err)

        api_endpoint = self.workflow_manager_host + "/api/metadata/workflow/{workflow_name}/{workflow_version}".format(
            workflow_name=workflow_name, workflow_version=workflow_version)
        response_received = requests.delete(api_endpoint)
        if response_received.status_code != 204:
            err = dict()
            err["message"] = response_received.text
            err["status_code"] = response_received.status_code
            raise Exception(err)

        return response_received.status_code


# if __name__ == '__main__':
#     ws = WorkflowService()
#     print(ws.get_all_workflows())
# print(WorkflowService.delete_workflow('pneumonia_workflow_01', 1))
