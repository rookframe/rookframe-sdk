extends Control
const SettingsScope = preload("res://rookframe/sdk/settings_scope.gd")
const SettingsDraft = preload("res://rookframe/sdk/settings_draft.gd")
## The containing menu owns save/cancel, authorization, validation and persistence.
var draft: SettingsDraft = SettingsDraft.new()
var scope: SettingsScope.Kind

func _rookframe_edit_settings(edit_scope: int, values: Dictionary) -> void:
	scope = edit_scope
	draft = SettingsDraft.new(values)
	edit()

func _rookframe_settings_values() -> Dictionary:
	return draft._copy()

## Override to populate the authored form from this scope's draft.
func edit() -> void:
	pass
