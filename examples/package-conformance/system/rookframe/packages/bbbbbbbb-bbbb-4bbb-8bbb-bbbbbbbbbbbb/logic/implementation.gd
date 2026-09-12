extends "res://rookframe/packages/bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb/sdk/implementation.gd"

func start() -> void:
	var device: SDK.DeviceExperience = sdk.presentation_experience()
	if device.is_desktop:
		print("Workshop System: desktop Edition 2028")
