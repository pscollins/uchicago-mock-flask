
function initPhotos(result_json) {
	var PHOTO_DOM_NODE = $("#photo-display");

	console.log("Got result json: " + result_json);
	console.log("Contains HTML: " + result_json.html);

	PHOTO_DOM_NODE.html(result_json.html);

	console.log("Set.");
};
