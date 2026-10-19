extends "res://rookframe/sdk/operation_result.gd"
## A completed outcome; pending state belongs to Rookframe.
var retry_after: int
func _init(result: Dictionary) -> void:
	super(result)
	retry_after = result.get("retry_after", 0)
