extends RefCounted

const RookId = preload("res://rookframe/sdk/rook_id.gd")
var rook_id: RookId
var label: String
func _init(value: Dictionary) -> void:
	rook_id = RookId.new(value.rookId)
	label = value.label
