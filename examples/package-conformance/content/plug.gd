extends "res://addons/gd-plug/plug.gd"

func request_quit(exit_code := -1) -> bool:
    return super.request_quit(0 if exit_code == -1 else exit_code)

func _plugging() -> void:
    # These examples choose the typed SDK. The Development Plugin installs independently.
    plug("rookframe/rookframe-sdk", {"tag": "v0.36.0-rc.4", "include": ["rookframe/sdk"]})
