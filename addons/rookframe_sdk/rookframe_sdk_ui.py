"""Typed additions to the editioned Package-local facade."""


def ui_sources(root: str) -> dict[str, str]:
    return {
        "contribution.gd": '''extends Resource

## An authored Control scene; Rookframe owns its integration lifetime.
@export var scene: PackedScene
''',
        "contribution_slot.gd": f'''extends RefCounted

const Contribution = preload("{root}contribution.gd")
var _host: Object
var _slot: String

func _init(host: Object, slot: String) -> void:
\t_host = host
\t_slot = slot

## Append an authored contribution in Package-local order. Repeated scenes are idempotent.
func push(entry: Contribution) -> void:
\t_host.RegisterContribution(_slot, entry.scene)
''',
        "slots.gd": f'''extends RefCounted

const ContributionSlot = preload("{root}contribution_slot.gd")
var _selected_rook: ContributionSlot
var _actor_creation: ContributionSlot
var selected_rook: ContributionSlot:
\tget:
\t\treturn _selected_rook
## Only the selected System Extension may contribute Actor Creation UI.
var actor_creation: ContributionSlot:
\tget:
\t\treturn _actor_creation

func _init(host: Object) -> void:
\t_selected_rook = ContributionSlot.new(host, "selected-rook")
\t_actor_creation = ContributionSlot.new(host, "actor-creation")
''',
        "feedback_action.gd": '''extends Resource

@export var id: String
@export var title: String
''',
        "feedback_message.gd": f'''extends Resource

const FeedbackAction = preload("{root}feedback_action.gd")
@export var title: String
@export_multiline var message: String
@export var actions: Array[FeedbackAction] = []
''',
        "feedback.gd": f'''extends RefCounted

const FeedbackMessage = preload("{root}feedback_message.gd")
signal action_selected(action: String)
var _request_id: int = 0
var _host: Object

func _init(host: Object) -> void:
\t_host = host
\t_host.connect("FeedbackActionSelected", _on_action)

func notice(message: FeedbackMessage) -> void:
\t_show(message, "notice")

func warning(message: FeedbackMessage) -> void:
\t_show(message, "warning")

func error(message: FeedbackMessage) -> void:
\t_show(message, "error")

func confirm(message: FeedbackMessage) -> void:
\t_show(message, "confirmation")

func _show(message: FeedbackMessage, severity: String) -> void:
\tvar actions: Array[Dictionary] = []
\tfor action in message.actions:
\t\tactions.append({{"id": action.id, "title": action.title}})
\t_request_id = _host.ShowFeedback(message.title, message.message, severity, actions)

func _on_action(request_id: int, action: String) -> void:
\tif request_id == _request_id:
\t\taction_selected.emit(action)
''',
        "translations.gd": '''extends RefCounted

var _host: Object

func _init(host: Object) -> void:
\t_host = host

## Translate within this Package's declared domain; missing messages retain their source text.
func text(message: String, domain: String = "default") -> String:
\treturn _host.Translate(message, domain)
''',
        "window.gd": f'''extends Control

const SDK = preload("{root}package_sdk_facade.gd")
## Bound by Rookframe before the authored window enters the tree. Null in the standalone editor.
var sdk: SDK

func _ready() -> void:
\tif has_meta("rookframe_sdk"):
\t\tsdk = SDK.new(get_meta("rookframe_sdk"))
\tready()

## Override for authored view setup; normal Godot child readiness has completed.
func ready() -> void:
\tpass
''',
        "cleanup.gd": '''extends RefCounted

var _completed: Callable
var _finished := false

func _init(completed: Callable) -> void:
\t_completed = completed

## Acknowledge immediate or asynchronous cleanup within the shared one-second deadline.
func complete() -> void:
\tif not _finished:
\t\t_finished = true
\t\t_completed.call()
''',
        "device_experience.gd": '''extends RefCounted

var _device: int
var is_desktop: bool:
\tget:
\t\treturn _device == 0
var is_tablet: bool:
\tget:
\t\treturn _device == 1
var is_phone: bool:
\tget:
\t\treturn _device == 2

func _init(device: int) -> void:
\t_device = device
''',
    }


def character_hud_sources(root: str) -> dict[str, str]:
    return {
        "character_hud_context.gd": f'''extends "{root}operation_result.gd"
const ActorId = preload("{root}actor_id.gd")
const RookId = preload("{root}rook_id.gd")
## Null Actor means there is no owned character context. Selection is never changed.
var actor: ActorId
var rook: RookId
func _init(result: Dictionary) -> void:
\tsuper(result)
\tif ok:
\t\tvar value: Dictionary = result.value
\t\tactor = ActorId.new(value.actor_id) if not str(value.actor_id).is_empty() else null
\t\trook = RookId.new(value.rook_id) if not str(value.rook_id).is_empty() else null
''',
        "character_hud.gd": f'''extends RefCounted
const Contribution = preload("{root}contribution.gd")
const CharacterHudContext = preload("{root}character_hud_context.gd")
const OperationResult = preload("{root}operation_result.gd")
signal context_changed
var _host: Object
func _init(host: Object) -> void:
\t_host = host
\t_host.CharacterHudContextChanged.connect(_changed)
func _changed() -> void:
\tcontext_changed.emit()
## The selected System may mount one authored full-rectangle Control, with mouse_filter IGNORE.
## It owns its children and hides its root for unsupported Actor types or empty context.
## Rookframe places it above floating tasks, below docks and full-viewport tasks.
func mount(entry: Contribution) -> void:
\t_host.RegisterContribution("character-hud", entry.scene)
## Owned selection first; sole-owned-Actor Player fallback; no GM default.
func context() -> CharacterHudContext:
\treturn CharacterHudContext.new(_host.CharacterHudContext())
## Open the existing native tray, preserving an already pending requested Throw.
func open_dice_tray() -> OperationResult:
\treturn OperationResult.new(_host.OpenDiceTray())
''',
    }
