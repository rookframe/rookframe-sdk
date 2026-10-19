extends "res://rookframe/sdk/operation_result.gd"

## Logical center-to-center distance in the current Scene's tabletop units.
var distance: float
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		distance = result.value
