extends "res://rookframe/sdk/settings_draft.gd"
const SettingsScope = preload("res://rookframe/sdk/settings_scope.gd")
var scope: SettingsScope.Kind
var source_version: String
var target_version: String
func _init(candidate_scope: SettingsScope.Kind, source: String, target: String, values: Dictionary) -> void:
	super(values)
	scope = candidate_scope
	source_version = source
	target_version = target
