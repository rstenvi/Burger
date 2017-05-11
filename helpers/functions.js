

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

			// Handle case where "/" is the path
			if(p != "/")	{var s = l.search(p);}
			else	{s = l.length-1;}

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
			for (var key in h)	{
				xhr.setRequestHeader(key, h[key]);
			}

			xhr.onreadystatechange = function() {
			    if(xhr.readyState == 4 && xhr.status == 200) {
			        if(cb)	cb(req, xhr);
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
			xhr.send("data=" + encodeURIComponent(result.responseText));
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

var Html = function()	{
	return	{
		extractId: function(html, fid)	{
			var el = document.createElement('html');
			return el.getElementById(fid);
		},

		// Extract the N'th instance of an element
		extractTagN: function(html, tag, N)	{
			var el = document.createElement('html');
			el.innerHTML = html;
			return el.getElementsByTagName(tag)[N];

		},
		extractAttribute: function(el, attr)	{
			if(el.hasAttribute(attr))	{
				return el.getAttribute(attr);
			}
			else	{
				return null;
			}
		},
		extractAttributesChilds: function(par, attrs, tag)	{
			var els = par.getElementsByTagName(tag);
			var ret = []
			for(var i = 0; i < els.length; i++)	{
				ins = {"tag": tag}
				for(var j = 0; j < attrs.length; j++)	{
					var val = this.extractAttribute(els[i], attrs[j]);
					if(val != null)	{
						ins[attrs[j]] = val;
//						ret.push({"tag": tag, attr:val});
					}
				}
				ret.push(ins)
			}
			return ret;
		},
		form2http: function(form)	{
			req = {
				"method":"POST",
				"resource":"/",
				"target":Browser.target_URL(),
				"enctype":"application/x-www-form-urlencoded"
			};
			if(form.hasAttribute("method"))	{
				req["method"] = form.getAttribute("method");
			}
			if(form.hasAttribute("action"))	{
				fa = form.getAttribute("action");
				if(fa.indexOf("http") == 0)	{
					ll = fa.indexOf("://")
					if(ll == -1)	{
						console.log("Error")
					}
					ll = fa.indexOf("/", ll+3);
					req["target"] = fa.substring(0, ll);
					req["resource"] = fa.substring(ll);
				}
				else	{
					req["resource"] = fa
				}
			}
			var inputs=[];
			var params = {}
			var elems=["select","input"];
			for(var i = 0; i < elems.length; i++)	{
				var l = this.extractAttributesChilds(form, ["name","value"], elems[i]);
				for(var j = 0; j < l.length; j++)	{
					inputs.push(l[j]);
					params[l[j]["attr"]] = "";
				}
			}
			req["inputs"] = inputs;
			req["params"] = params;
			return req;
		}
	};
}();

var Scanner = function()	{
	return	{
		findServer: function(ip, port, url, to, cb_loaded)	{
			var img = new Image();
			img.onerror = function () {
				if (!img) return;
				img = undefined;
				console.log('error');
			};
			img.onload = function () {
				if (!img) return;
				console.log(img);
				img = undefined;
				console.log('loaded');
				cb_loaded(ip, port);
			};
	
			img.src = 'http://' + ip + ':' + port + url;
			setTimeout(function () {
				if (!img) return;
				img = undefined;
				console.log('closed');
			}, to);
		}
	  };
}();




