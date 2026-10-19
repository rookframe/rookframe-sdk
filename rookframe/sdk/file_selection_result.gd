extends "res://rookframe/sdk/integration_result.gd"
const ScopedFile = preload("res://rookframe/sdk/scoped_file.gd")

var file: ScopedFile
func _init(result: Dictionary, selection: ScopedFile) -> void:
	super(result)
	file = selection
