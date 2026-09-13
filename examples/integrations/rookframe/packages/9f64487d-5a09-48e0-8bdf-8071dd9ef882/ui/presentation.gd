extends "res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/sdk/presentation.gd"

const WINDOW_BUTTON: SDK.WindowButton = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/ui/window_button.tres")


func compose() -> void:
	var rail: SDK.Rail = sdk.rails.left
	rail.push(WINDOW_BUTTON)
