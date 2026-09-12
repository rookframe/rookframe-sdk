extends "res://rookframe/packages/dddddddd-dddd-4ddd-8ddd-dddddddddddd/sdk/presentation.gd"
const UI_ROOT: SDK.Contribution = preload("res://rookframe/packages/dddddddd-dddd-4ddd-8ddd-dddddddddddd/ui/ui_root.tres")

func compose() -> void:
	sdk.ui_root.push(UI_ROOT)

