extends Resource

const ExtensionSurface = preload("res://rookframe/sdk/extension_surface.gd")
## Authored Button scene, using the public UI Kit Theme and assets.
@export var button_scene: PackedScene
## The window to open when this entry is activated.
@export var window: ExtensionSurface
