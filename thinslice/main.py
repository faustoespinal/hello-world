from flask import Flask, request, render_template, jsonify, Response
from inferencing.inferencing_service import InferencingService
from workflow.workflow_service import WorkflowService
import json
import os
app = Flask(__name__,static_folder=os.path.abspath('static/'))

@app.route("/")
def engine_status():
    context=dict()
    context["qido_url"]=os.environ.get("QIDO_URL","")
    context["workflow_url"]=os.environ.get("WORKFLOW_URL","")
    context["imaging_url"]=os.environ.get("IMAGING_URL","")
    context["imaging_host_url"]=os.environ.get("IMAGING_HOST_URL","")
    return render_template("index.html",data=context)


@app.route("/inference/execute", methods=["POST"])
def run_inferencing_workflow():
    try:
        request_json_object = request.get_json()
        workflow_id = request_json_object.get("workflowId")
        study = request_json_object.get("study")
        series = request_json_object.get("series")

        if workflow_id is None or workflow_id == "":
            raise Exception("Workflow ID not provided")

        if study is None or study == "":
            raise Exception("Study not provided")

        if series is None or series == "":
            raise Exception("Series not provided")

        message = InferencingService().run_inferencing_workflow(workflow_id,1, series, study)
        response = Response(response=json.dumps(message), status=200,
                            mimetype='application/json')
    except Exception as exp:
        response = Response(response=json.dumps(str(exp)),status=400,
                            mimetype='application/json')
    return response


@app.route("/inference/<workflowCorrelationId>/status", methods=["GET"])
def get_workflow_status(workflowCorrelationId):
    try:
        if workflowCorrelationId is None or workflowCorrelationId == "":
            raise Exception("Workflow Correlation ID not provided")
        print(workflowCorrelationId)
        message = InferencingService().get_workflow_status(workflowCorrelationId)
        response = Response(response=json.dumps(message), status=200,
                            mimetype='application/json')
    except Exception as exp:
        response = Response(response=json.dumps(str(exp)), status=400,
                            mimetype='application/json')
    return response


@app.route("/inference/active", methods=["GET"])
def get_all_active_workflow():
    try:
        message = InferencingService().get_all_active_workflow()
        response = Response(response=json.dumps(message), status=200,
                            mimetype='application/json')
    except Exception as exp:
        response = Response(response=json.dumps(str(exp)), status=400,
                            mimetype='application/json')
    return response


@app.route("/inference/cancel", methods=["POST"])
def terminate_workflow():
    try:
        workflow_correlation_id_array = request.get_json()
        message = InferencingService().terminate_workflow(workflow_correlation_id_array)
        response = Response(response=json.dumps(message), status=200,
                            mimetype='application/json')
    except Exception as exp:
        response = Response(response=json.dumps(str(exp)), status=400,
                            mimetype='application/json')
    return response


@app.route("/workflow/list", methods=["GET"])
def get_all_workflows():
    try:
        workflow_correlation_id_array = request.get_json()
        message = WorkflowService().get_all_workflows()
        response = Response(response=json.dumps(message), status=200,
                            mimetype='application/json')
    except Exception as exp:
        response = Response(response=json.dumps(str(exp)), status=400,
                            mimetype='application/json')
    return response


@app.route("/workflow/<workflow_name>/delete", methods=["POST"])
def delete_workflow(workflow_name):
    try:
        message = WorkflowService().delete_workflow(workflow_name,workflow_version=1)
        response = Response(response=json.dumps(message), status=200,
                            mimetype='application/json')
    except Exception as exp:
        response = Response(response=json.dumps(str(exp)), status=400,
                            mimetype='application/json')
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
