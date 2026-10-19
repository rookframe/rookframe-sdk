extends "res://rookframe/sdk/operation_result.gd"

const ContentEntry = preload("res://rookframe/sdk/content_entry.gd")
var items: Array[ContentEntry] = []
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_values: Array = result.value
		for value in raw_values:
			items.append(ContentEntry.new(value))
