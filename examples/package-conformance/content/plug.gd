extends "res://addons/gd-plug/plug.gd"


# Read the repository's single dependency setting directly.
var ui_kit = load(ProjectSettings.globalize_path("res://.rookframe/rookframe_ui_kit.gd" if FileAccess.file_exists("res://.rookframe/rookframe_ui_kit.gd") else "res://../../../../tools/rookframe_ui_kit.gd")).new()


func _initialize() -> void:
	if ui_kit.dependency.is_empty():
		quit(1)
		return
	super._initialize()


func request_quit(exit_code := -1) -> bool:
	if not threadpool.is_all_thread_finished() or not threadpool.is_all_task_finished():
		return false
	var result := 0 if exit_code == -1 else exit_code
	var args := OS.get_cmdline_args()
	if result == 0 and ("install" in args or "update" in args):
		result = ui_kit.write_provenance(false)
	return super.request_quit(result)


func _plugging() -> void:
	plug("rookframe/rookframe-sdk", {"tag": "v0.12.0", "include": ["addons/rookframe_sdk"]})
	plug("rookframe/rookframe-ui-kit", ui_kit.options())


func install_plugin(plugin):
	if plugin.name == "rookframe-ui-kit":
		ui_kit.install(self, plugin)
	else:
		super.install_plugin(plugin)


func update_plugin(plugin, checking=false):
	if plugin.name == "rookframe-ui-kit":
		if not checking:
			ui_kit.install(self, plugin)
		return false
	return super.update_plugin(plugin, checking)
