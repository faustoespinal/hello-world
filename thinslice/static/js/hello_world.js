
//EHL BASE URL - Change this value
//var ehl_base_url = "http://andromeda.edison.health.ge.com";
var ehl_base_url = "http://10.12.40.104";
var neww = "{{data.qido_url}}";
var URL = {
    eis_qido: ehl_base_url + ":30043/eis/v1/store",
    image_viewer: ehl_base_url + ":32701/lite-viewer/?port=32710&store=Edison&study=",
    workflow_conductor: ehl_base_url + ":30180/api/workflow",
    workflow_conductor_metadata: ehl_base_url + ":30180/api/metadata/workflow"
}

var selectedStudyUID;
var selectedSeriesUID;
var selectedWorkflowName;
var selectedWorkflowVersion;


//Add initial functionality to page elements on page load
function setInitialParameters() {

    document.getElementById("imageBrowserTab").click();
    document.getElementById("myLoader").style.visibility = "hidden";
    getStudies(URL.eis_qido + "/EIS.DCM/studies/?includeField=00100020,00100010,00081030,00200010,00080020,00080060");  

    window.addEventListener("click", function (event) {
        if (!event.target.matches('.dropbutton')) {
            var dropdown = document.getElementById("myDropdownContent");
            if (dropdown.classList.contains('show')) {
                dropdown.classList.remove('show');
            }
        }
    });
}

//HTTP Request Functions

//Call an HTTP GET Request and asynchronously sends the response to another function
function httpGet(url, callback) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
            callback(http.responseText);
        }
    };
    http.open('GET', url, true);
    http.send();
}

//Call an HTTP POST Request and asynchronously sends the response to another function
function httpPOST(url, callback, payload) {
    var http = new XMLHttpRequest();
    http.onreadystatechange = function () {
        if (http.readyState == 4 && http.status == 200) {
            callback(http.responseText);
        }
    };
    http.open('POST', url, true);
    http.setRequestHeader('Content-Type', 'application/json');
    http.send(payload);
}


//DROPDOWN
function getWorkflows() {
    httpGet(URL.workflow_conductor_metadata, populateWorkflowDropdown);
}

//Populates the workflow dropdown
function populateWorkflowDropdown(data) {

    var dropdown = document.getElementById("myDropdown");
    var dropdownContent = document.getElementById("myDropdownContent");

    if (dropdownContent.childElementCount != 0) {
        dropdown.removeChild(dropdownContent);
        dropdownContent = document.createElement("div");
        dropdownContent.setAttribute("id", "myDropdownContent");
        dropdownContent.setAttribute("class", "dropdown-content");
    }

    var JSONdata = JSON.parse(data);
    for (var i = 0; i < JSONdata.length; i++) (function (i) {
        
        var a = document.createElement("a");
        a.innerHTML = JSONdata[i].name;

        a.onclick = function () {
            selectedWorkflowName = JSONdata[i].name;
            selectedWorkflowVersion = JSONdata[i].version;
            document.getElementById("myDropdownButton").innerHTML = event.target.innerHTML;
        };
        dropdownContent.appendChild(a);
    })(i);

    dropdown.appendChild(dropdownContent);
    dropdownContent.classList.toggle("show");
}

//TABS
//Handles page transitions by tab clicks
function openPageByTab(event, tabName) {
    var i, tabcontent, tablinks;

    if (tabName == "imageViewer") {
        applyImageViewer();
    }

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("masthead-tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" tab-selected", "");
    }
    document.getElementById(tabName).style.display = "block";
    event.currentTarget.className += " tab-selected";
}


//TABLES
//QIDO studies and populate study table
function getStudies(url) {
    tableId = "studyTable";
    httpGet(url, populateTable);
}

//QIDO series and populate series table
function getSeries(url) {
    tableId = "seriesTable";
    httpGet(url, populateTable);
}


function populateTable(data) {

    JSONdata = JSON.parse(data);
    var table = document.getElementById(tableId);

    var tbody = table.getElementsByTagName("tbody")[0];
    if (tbody != null) {
        table.removeChild(tbody);
    }

    if (JSONdata.length > 0) {

        tbody = document.createElement("tbody");
        var bRow = [];
        for (var i = 0; i < JSONdata.length; i++) (function (i) {
            bRow[i] = document.createElement("tr");

            if (this.tableId == "studyTable") {
                populateStudyRow(bRow[i], JSONdata[i]);
            } else if (this.tableId == "seriesTable") {
                populateSeriesRow(bRow[i], JSONdata[i]);
            }

            tbody.appendChild(bRow[i]);
        })(i);

        table.appendChild(tbody);
    }
}


function populateStudyRow(row, data) {

    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.study_uid, data);
    row.appendChild(td);
    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.patient_name, data);
    row.appendChild(td);
    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.patient_id, data);
    row.appendChild(td);
    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.study_date, data);
    row.appendChild(td);
    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.study_description, data);
    row.appendChild(td);

    row.onclick = function () {
        highlightRow(row);
        selectedStudyUID = getDICOMValue(DICOM_DICTIONARY.study_instance_uid, data);
        console.log(selectedStudyUID);
        selectedSeriesUID = null;
        url = URL.eis_qido + "/EIS.DCM/studies/" + selectedStudyUID + "/series?includeField=0008103E,0020000E,00200011,00201209";
        getSeries(url);
    };
}


function populateSeriesRow(row, data) {

    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.series_number, data);
    row.appendChild(td);
    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.series_description, data);
    row.appendChild(td);
    var td = document.createElement("td");
    td.innerHTML = getDICOMValue(DICOM_DICTIONARY.number_of_series_related_instances, data);
    row.appendChild(td);

    row.onclick = function () {
        highlightRow(row);
        selectedSeriesUID = getDICOMValue(DICOM_DICTIONARY.series_instance_uid, data);
        console.log(selectedSeriesUID);
    };
}


function highlightRow(row) {

    table = row.parentNode.parentNode;
    for (var i = 0; i < table.rows.length; i++) {
        table.rows[i].classList.remove("selected");
    }
    row.classList.add("selected");
}


//Helper function for parsing DICOM Data
function getDICOMValue(tag, jsonData) {
    var value = "";

    if (typeof (jsonData[tag]) !== 'undefined') {
        var value = jsonData[tag].Value;
        if (jsonData[tag].vr == "PN") {
            for (var i = 0; i < value.length; i++) {
                value[i] = value[i].Alphabetic;
            }
        }
        if (jsonData[tag].vr == "DA" && value.length !== 0) {

            var date = value.toString();
            value = date.substring(4, 6) + "/" + date.substring(6, 8) + "/" + date.substring(0, 4);
        }
    }

    return value;
}



//IMAGE FABRIC VIEWER
//Apply the Image Fabric Viewer to an Iframe
function applyImageViewer() {

    if (selectedSeriesUID != null) {
        var url = URL.image_viewer + selectedStudyUID.toString() + '&series=' + selectedSeriesUID;
        var iframe = document.getElementById('imageViewerFrame');
        iframe.setAttribute('src', url);
    } else if (selectedStudyUID != null) {
        var url = URL.image_viewer + selectedStudyUID.toString();
        var iframe = document.getElementById('imageViewerFrame');
        iframe.setAttribute('src', url);
    }
}

//WORKFLOW
//Execute workflow in conductor with currently selected study and series
function executeWorkflow() {

    var workflowButton = document.getElementsByClassName("workflow-button");
    if (workflowButton.disabled == true) {
        alert('Please wait for workflow to finish executing');
    }

    if (selectedStudyUID == null || selectedSeriesUID == null) {
        alert('Please select study and series before executing workflow');
    } else if (selectedWorkflowName == null || selectedWorkflowVersion == null) {
        alert('Please select workflow type');
    } else {

        let correlationId = generateCorrelationId();
        let numTasks = 3;

        var payload = JSON.stringify({
            'name': selectedWorkflowName,
            'version': selectedWorkflowVersion,
            'correlationId': correlationId,
            'numberOfTasks': numTasks,
            'input': {
                'study': selectedStudyUID.toString(),
                'series': selectedSeriesUID.toString()
            }
        });

        httpPOST(URL.workflow_conductor, checkWorkflowStatus, payload);
    }
}


var interval;
//Repeatedly calls the updateWorkflowStatus function with responses from GET requests to workflow conductor
function checkWorkflowStatus(workflowId) {
    var workflowInfoURL = URL.workflow_conductor + "/" + workflowId;

    interval = setInterval(function () {
        httpGet(workflowInfoURL, updateWorkflowStatus);
    }, 1000);
}

//Updates the workflow status indicators on the UI
function updateWorkflowStatus(workflowResponse) {

    var JSONresponse = JSON.parse(workflowResponse);
    var statusIndicator = document.getElementById("myWorkflowStatus");
    var statusLoader = document.getElementById("myLoader");
    var statusLoaderBar = document.getElementById("myLoaderBar");
    var status = JSONresponse.status;
    statusIndicator.innerHTML = status;

    var workflowButton = document.getElementById("myWorkflowButton");
    var tasks = JSONresponse.tasks;
    var numTasks = JSONresponse.workflowDefinition.tasks.length;
    
    if (status == "RUNNING") {
        statusLoader.style.visibility = "visible";
        workflowButton.disabled = true;

        for (var i = 0; i < tasks.length; i++) {
           
            if (tasks[i].status == "SCHEDULED" || (tasks[i].status == "COMPLETED" && typeof tasks[i + 1] == 'undefined') || (tasks[i].status == "FAILED" && typeof tasks[i + 1] == 'undefined')) {
                if (tasks[0].status == "SCHEDULED") {
                    updateStatusBar(statusLoaderBar, 0);
                }
                statusIndicator.innerHTML = status + ": " + tasks[i].referenceTaskName;
            } else if (tasks[i].status == "COMPLETED") {
                updateStatusBar(statusLoaderBar, (i + 1) / numTasks);
            }
        }

    } else if (status == "COMPLETED") {
        updateStatusBar(statusLoaderBar, 1);
        workflowButton.disabled = false;

        //update series table
        var series_url = URL.eis_qido + "/EIS.DCM/studies/" + selectedStudyUID + "/series?includeField=0008103E,0020000E,00200011,00201209";
        getSeries(series_url);
        clearInterval(interval);

        //update results
        for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].referenceTaskName == "ai_inferencing") {
                statusIndicator.innerHTML = status + " " + tasks[i].outputData.response.body.prediction[0].geClass + ": Probability = " + tasks[i].outputData.response.body.prediction[0].probability;
            }
        }
        
    } else {
        updateStatusBar(statusLoaderBar, 1);
        workflowButton.disabled = false;
        clearInterval(interval);
        for (var i = 0; i < tasks.length; i++) {
            if (tasks[i].outputData.response.reasonPhrase == "BAD REQUEST") {
                alert(status + ": " + tasks[i].outputData.response.body.message);
            }
        }
    }
}

function updateStatusBar(bar, progress) {
    var barWidth = bar.parentNode.offsetWidth * progress;
    bar.setAttribute("style", "width: " + barWidth + "px;");
}


function generateCorrelationId() {
    return [...Array(20)].map(i => (~~(Math.random() * 36)).toString(36)).join('');
}



var DICOM_DICTIONARY = {

    patient_id: "00100020",
    patient_name: "00100010",

    study_description: "00081030",
    study_instance_uid: "0020000D",
    study_uid: "00200010",
    study_date: "00080020",

    series_description: "0008103E",
    series_instance_uid: "0020000E",
    series_number: "00200011",

    number_of_series_related_instances: "00201209"
}

