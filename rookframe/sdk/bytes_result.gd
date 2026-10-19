extends "res://rookframe/sdk/integration_result.gd"
var data: PackedByteArray = []
func _init(result: Dictionary) -> void:
	super(result)
	data = result.get("data", [])
