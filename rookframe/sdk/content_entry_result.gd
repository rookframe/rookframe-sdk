extends "res://rookframe/sdk/operation_result.gd"

const ContentEntry = preload("res://rookframe/sdk/content_entry.gd")
var content_entry: ContentEntry
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_value: Dictionary = result.value
		content_entry = ContentEntry.new(raw_value)
