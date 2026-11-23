extends "res://rookframe/sdk/integration_result.gd"

## May be null on success. Use ok to distinguish a null payload from failure.
var value: Variant

func _init(result: Dictionary) -> void:
	super(result)
	value = result.get("value")
