extends "res://rookframe/sdk/integration_result.gd"
var text: String
func _init(result: Dictionary) -> void:
	super(result)
	text = result.get("text", "")
