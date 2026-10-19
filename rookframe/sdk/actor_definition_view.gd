extends RefCounted
const ExtensionSurface = preload("res://rookframe/sdk/extension_surface.gd")
## System-owned Library presentation. An empty category omits a workflow-only definition.
var category: String
var surface: ExtensionSurface
var can_create: bool
func _init(label: String = "", window: ExtensionSurface = null, creatable: bool = false) -> void:
	category = label
	surface = window
	can_create = creatable
