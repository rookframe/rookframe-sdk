extends RefCounted
const Contribution = preload("res://rookframe/sdk/contribution.gd")
const CharacterHudContext = preload("res://rookframe/sdk/character_hud_context.gd")
const OperationResult = preload("res://rookframe/sdk/operation_result.gd")
signal context_changed
var _host: Object
func _init(host: Object) -> void:
	_host = host
	_host.CharacterHudContextChanged.connect(_changed)
func _changed() -> void:
	context_changed.emit()
## The selected System may mount one authored full-rectangle Control, with mouse_filter IGNORE.
## It owns its children and hides its root for unsupported Actor types or empty context.
## Rookframe places it above floating tasks, below docks and full-viewport tasks.
func mount(entry: Contribution) -> void:
	_host.RegisterContribution("character-hud", entry.scene)
## Owned selection first; sole-owned-Actor Player fallback; no GM default.
func context() -> CharacterHudContext:
	return CharacterHudContext.new(_host.CharacterHudContext())
## Open the existing native tray, preserving an already pending requested Throw.
func open_dice_tray() -> OperationResult:
	return OperationResult.new(_host.OpenDiceTray())
