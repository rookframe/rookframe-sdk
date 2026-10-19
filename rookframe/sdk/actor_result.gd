extends "res://rookframe/sdk/operation_result.gd"

const Actor = preload("res://rookframe/sdk/actor.gd")
var actor: Actor
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_value: Dictionary = result.value
		actor = Actor.new(raw_value)
