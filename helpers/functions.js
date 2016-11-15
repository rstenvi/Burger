

var Cookie = function()	{
	return {
		getAll: function()	{
			var ret = {};
			var cookies = document.cookie.split(";");
			for(var i = 0; i < cookies.length; i++)	{
				var cookie = cookies[i].trim();
				var vals = cookie.split("=");
				ret[vals[0]] = vals[1];
			}
			return ret;
		},
		getNamed: function(name)	{
			var cookies = this.getAll();
			return cookies[name];

		},
	};
}();


// General interaction with the browser
var Browser = function()	{
	return	{
		// Get current target in the form of:
		// - https://example.com
		target_URL: function()	{
			var l = window.location.toString();
			var p = window.location.pathname.toString();
			var s = l.search(p);
			return l.substring(0,s);
		}
	};
}();




var Network = function()	{
	return {
		request: function(req, cb)	{
			var xhr = new XMLHttpRequest();
			xhr.open(req["method"], req["target"] + req["resource"], true);

			// If not present, there are no headers
			h = {}
			if("headers" in req)	h = req["headers"];
			for (var key in req["headers"])	{
				xhr.setRequestHeader(key, headers[key]);
			}

			xhr.onreadystatechange = function() {
			    if(xhr.readyState == 4 && xhr.status == 200) {
			        if(cb)	cb(req, xhr.responseText);
			    }
			}

			// We check if params exist, if not we assume null
			p = null;
			if("params" in req)	p = req["params"];
			xhr.send(p);
		},
		sendHome: function(origReq, result)	{
			var xhr = new XMLHttpRequest();
			xhr.open(returnPath["method"], returnPath["target"] + returnPath["resource"], true);
			xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
			xhr.onreadystatechange = function() {
			    if(xhr.readyState == 4 && xhr.status == 200) {
			        console.log(xhr.responseText);
			    }
			}
			// Send as URL-encoded
			xhr.send("data=" + encodeURIComponent(result));
		}
	};
}();



var Data = function()	{
	return {
		serialize: function(d)	{
			var strs = []
			for(var k in d)	{
				strs.push(encodeURIComponent(k) + "=" + encodeURIComponent(d[k]))
			}
			return strs.join("&")
		}
	};
}();



