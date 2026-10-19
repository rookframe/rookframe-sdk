extends "res://rookframe/sdk/operation_result.gd"

## Only the owning Package interprets this value. This is not a host object.
var value: Variant
func _init(result: Dictionary) -> void:
	super(result)
	value = result.get("value")
