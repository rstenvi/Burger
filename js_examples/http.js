

var req = {
	"method":"GET",
	"target":Browser.target_URL(),
	"resource":"/"
};

Network.request(req,Network.sendHome);

