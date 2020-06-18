import os

edgeBox_BASE_URL = 'http://10.12.40.157'
APP_ENV = os.environ.get('APP_ENV', 'Dev')
WORKFLOW_MANGER_HOST = os.environ.get('WORKFLOW_MANGER_HOST', "http://10.12.40.157:30180")
QIDO_URL = edgeBox_BASE_URL + ':30043'
EAI_IS =  edgeBox_BASE_URL + ':30333'
