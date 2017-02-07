

var fs = require('fs')
var jsdom = require("jsdom").jsdom;
var request = require("request");
var document;
var window;


function html2forms(html)	{
	document = jsdom(html);
	window = document.defaultView;
	var reqs = [];
	var form = undefined;
	var form = Html.extractTagN(html, "form", 0);
	for(i = 1; form != undefined; i++)	{
		reqs.push(Html.form2http(form));
		form = Html.extractTagN(html, "form", i);
	}

	for(i = 0; i < reqs.length; i++)	{
		console.log(reqs[i]);
	}
	process.exit();
}

function parse_url(u)	{
	request(u, function (error, response, body) {
		if (!error) {
			html2forms(body);
		} else {
			console.log(error);
		}
	});
}


// Evaluate the source code used
eval(fs.readFileSync('helpers/functions.js')+'');


var argv = require('minimist')(process.argv.slice(2));

u=argv["url"]
if(u != undefined)	{
	console.log("Parsing URL: " + u);
	parse_url(u);
}
else	{
	console.log("ERROR: Need to provide a URL");
	console.log("nodejs form2req.js --url=<url>");
}

return 0;

// To read local file instead
// var html = fs.readFileSync('index.html')

