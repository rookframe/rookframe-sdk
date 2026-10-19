extends "res://rookframe/sdk/operation_result.gd"

const TargetSnapshot = preload("res://rookframe/sdk/target_snapshot.gd")

var snapshot: TargetSnapshot
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		snapshot = TargetSnapshot.new(result.value)
