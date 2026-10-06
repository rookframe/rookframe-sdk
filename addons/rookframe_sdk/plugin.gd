@tool
extends EditorPlugin

var _development: Control
var _dock: EditorDock

func _enter_tree() -> void:
	if OS.get_environment("ROOKFRAME_AUTHOR_COPY") == "1":
		return
	add_tool_menu_item("Rookframe: Check Package", _check)
	add_tool_menu_item("Rookframe: Build Package", _build_package)
	if FileAccess.file_exists("res://rookframe.json"):
		_run("facade")
		if FileAccess.file_exists("res://.rookframe/development.json"):
			# Apply project metadata during editor startup, before GameView reads it.
			var settings := EditorInterface.get_editor_settings()
			settings.set_project_metadata("game_view", "embed_on_play", true)
			settings.set_project_metadata("game_view", "make_floating_on_play", false)
		_dock = preload("res://addons/rookframe_sdk/development.tscn").instantiate()
		_development = _dock.get_node("Scroll/Content")
		add_dock(_dock)
		add_tool_menu_item("Rookframe: Development World", _dock.make_visible)


func _exit_tree() -> void:
	if OS.get_environment("ROOKFRAME_AUTHOR_COPY") == "1":
		return
	remove_tool_menu_item("Rookframe: Check Package")
	remove_tool_menu_item("Rookframe: Build Package")
	if is_instance_valid(_dock):
		remove_tool_menu_item("Rookframe: Development World")
		remove_dock(_dock)
		_dock.queue_free()


func _build() -> bool:
	return not is_instance_valid(_development) or _development.can_run()


func _check() -> void:
	_run("check")


func _build_package() -> void:
	_run("build")


func _run(command: String) -> void:
	# The CLI executes author tools only inside disposable project copies.
	# ROOKFRAME_PYTHON may name Python on installations without python3 on PATH.
	var python := OS.get_environment("ROOKFRAME_PYTHON")
	if python.is_empty():
		python = "python" if OS.get_name() == "Windows" else "python3"
	var output: Array = []
	var status := OS.execute(python, PackedStringArray([
		"-X", "utf8",
		ProjectSettings.globalize_path("res://addons/rookframe_sdk/rookframe_authoring.py"),
		command, "--project", ProjectSettings.globalize_path("res://"),
		"--godot", OS.get_executable_path(),
	]), output, true)
	for line in output:
		print(line)
	if status != 0:
		push_error("Rookframe " + command + " failed. See the Output panel for the corrective diagnostic.")
