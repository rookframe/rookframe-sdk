extends "res://rookframe/sdk/operation_result.gd"

const Actor = preload("res://rookframe/sdk/actor.gd")
var items: Array[Actor] = []
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_values: Array = result.value
		for value in raw_values:
			items.append(Actor.new(value))
