extends Resource

const ExtensionSurface = preload("res://rookframe/sdk/extension_surface.gd")
## Authored native Godot Button scene. Theme and assets are chosen by the author.
@export var button_scene: PackedScene
## The window to open when this entry is activated.
@export var window: ExtensionSurface
