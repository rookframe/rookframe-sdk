extends "res://rookframe/sdk/operation_result.gd"

const Scene = preload("res://rookframe/sdk/scene.gd")
var scene: Scene
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_value: Dictionary = result.value
		scene = Scene.new(raw_value)
