extends "res://rookframe/sdk/text_result.gd"
var found: bool
func _init(result: Dictionary) -> void:
	super(result)
	found = result.get("found", false)
