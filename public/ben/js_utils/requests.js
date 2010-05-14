var http_request = false;
function makeRequest(url, parameters) {
    http_request = false;
    if (window.XMLHttpRequest) { // Mozilla, Safari,...
        http_request = new XMLHttpRequest();
        if (http_request.overrideMimeType) {
            // set type accordingly to anticipated content type
            //http_request.overrideMimeType('text/xml');
            http_request.overrideMimeType('text/html');
        }
    } 
    if (!http_request) {
        alert('Cannot create XMLHTTP instance');
        return false;
    }
    http_request.onreadystatechange = alertContents;
    http_request.open('GET', url + parameters, true);
    http_request.send(null);
    //this is not at all efficient as it pauses all 

}
function alertContents() {
    if (http_request.readyState == 4) {
        if (http_request.status == 200) {
            //alert(http_request.responseText);
            result = http_request.responseText;
            document.getElementById('myspan').innerHTML =  result;            
        } else {
            alert('There was a problem with the request');
        }
    }
}