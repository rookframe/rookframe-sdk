extends "res://addons/gd-plug/plug.gd"


func request_quit(exit_code := -1) -> bool:
	return super.request_quit(0 if exit_code == -1 else exit_code)


func _plugging() -> void:
	plug("rookframe/rookframe-sdk", {"tag": "v0.3.0", "include": ["addons/rookframe_sdk"]})
	plug("rookframe/rookframe-ui-kit", {"commit": "238339d390ec01873585c002917c164948a0578d", "include": ["rookframe/ui"]})
