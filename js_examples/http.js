

// Get index page and return result
var request = {};
request["method"] = "GET";
request["target"] = target_URL();
request["resource"] = "/";
console.log(request)

sendRequest(request,null,null,returnData);

