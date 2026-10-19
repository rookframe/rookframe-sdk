extends "res://rookframe/sdk/portrait_result.gd"
## A retained World-relative filepath. Save this value through ordinary Actor data.
var path: String
func _init(result: Dictionary) -> void:
	super(result)
	path = result.get("path", "")
