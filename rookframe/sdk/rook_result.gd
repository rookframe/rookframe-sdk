extends "res://rookframe/sdk/operation_result.gd"

const Rook = preload("res://rookframe/sdk/rook.gd")
var rook: Rook
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_value: Dictionary = result.value
		rook = Rook.new(raw_value)
