extends "res://rookframe/sdk/operation_result.gd"
const SceneAtmosphere = preload("res://rookframe/sdk/scene_atmosphere.gd")

## Copied artistic intent. Editing this Resource has no effect until set_scene().
var atmosphere: SceneAtmosphere
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		atmosphere = SceneAtmosphere.new()
		atmosphere.read_record(result.value)
