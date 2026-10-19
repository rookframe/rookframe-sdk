extends "res://rookframe/sdk/operation_result.gd"

const Rook = preload("res://rookframe/sdk/rook.gd")
var items: Array[Rook] = []
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_values: Array = result.value
		for value in raw_values:
			items.append(Rook.new(value))
