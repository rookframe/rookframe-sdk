extends Resource

## Identity is scoped to this Package. Names are editable presentation text.
@export var id: String
@export var display_name: String
@export var icon: Texture2D
## Explicit order within this provider; tied orders use the stable id.
@export var order: int = 0
@export var mode: String = "all"
@export var role: String = "all"
@export var subject: String = "all"
## Authored full-rectangle Control. The host retains this instance between switches.
@export var scene: PackedScene

func definition() -> Dictionary:
	return {"id": id, "name": display_name, "icon": icon.resource_path if icon else "",
		"order": order, "mode": mode, "role": role, "subject": subject}
