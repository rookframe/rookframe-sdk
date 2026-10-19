extends "res://rookframe/sdk/integration_result.gd"
## A decoded native image for local presentation. No Script/Resource file is evaluated.
var texture: Texture2D
func _init(result: Dictionary) -> void:
	super(result)
	texture = result.get("texture", null)
