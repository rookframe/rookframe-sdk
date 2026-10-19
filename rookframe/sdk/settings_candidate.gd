extends "res://rookframe/sdk/settings_values.gd"
const SettingsScope = preload("res://rookframe/sdk/settings_scope.gd")
var scope: SettingsScope.Kind
func _init(candidate_scope: SettingsScope.Kind, values: Dictionary) -> void:
	super(values)
	scope = candidate_scope
