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
