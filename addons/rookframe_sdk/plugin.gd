@tool
extends EditorPlugin


func _enter_tree() -> void:
	if OS.get_environment("ROOKFRAME_AUTHOR_COPY") == "1":
		return
	add_tool_menu_item("Rookframe: Check Package", _check)
	add_tool_menu_item("Rookframe: Build Package", _build_package)
	if FileAccess.file_exists("res://rookframe.json"):
		_run("facade")


func _exit_tree() -> void:
	if OS.get_environment("ROOKFRAME_AUTHOR_COPY") == "1":
		return
	remove_tool_menu_item("Rookframe: Check Package")
	remove_tool_menu_item("Rookframe: Build Package")


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
		ProjectSettings.globalize_path("res://addons/rookframe_sdk/rookframe_authoring.py"),
		command, "--project", ProjectSettings.globalize_path("res://"),
		"--godot", OS.get_executable_path(),
	]), output, true)
	for line in output:
		print(line)
	if status != 0:
		push_error("Rookframe " + command + " failed. See the Output panel for the corrective diagnostic.")
	get_editor_interface().get_resource_filesystem().scan()
