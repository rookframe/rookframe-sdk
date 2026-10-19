extends RefCounted

const SceneId = preload("res://rookframe/sdk/scene_id.gd")
var id: SceneId
var name: String
func _init(value: Dictionary) -> void:
	id = SceneId.new(value.id)
	name = value.name
