extends "res://rookframe/sdk/operation_result.gd"

var sequence: int = 0
func _init(outcome: Dictionary) -> void:
	super(outcome)
	if ok:
		sequence = outcome.value.get("sequence", 0)
