extends RefCounted
const ContentReference = preload("res://rookframe/sdk/content_reference.gd")

## Presentation-only identity for Rookframe's native Actor list.
var display_name: String
var portrait: Texture2D
var miniature: ContentReference
var can_place: bool
func _init(name: String = "", image: Texture2D = null, model: ContentReference = null, placeable: bool = false) -> void:
	display_name = name
	portrait = image
	miniature = model
	can_place = placeable
