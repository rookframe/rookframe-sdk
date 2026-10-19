extends "res://rookframe/sdk/integration_result.gd"
const ScopedFolder = preload("res://rookframe/sdk/scoped_folder.gd")

var folder: ScopedFolder
func _init(result: Dictionary, selection: ScopedFolder) -> void:
	super(result)
	folder = selection
