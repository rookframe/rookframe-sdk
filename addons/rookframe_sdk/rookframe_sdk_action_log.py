"""Edition 2029 revision 5: deliberately publish bounded, non-interactive outcomes."""


def action_log_sources(root: str) -> dict[str, str]:
    return {
        "action_log_text.gd": '''extends Resource

## Printable text, with normal, strong, or emphasis formatting. Never markup.
@export var text: String
@export var style: String = "normal"
func _init(value: String = "", formatting: String = "normal") -> void:
\ttext = value
\tstyle = formatting
''',
        "action_log_die.gd": '''extends Resource

## One raw face in caller-supplied order; publishing does not roll dice.
@export var sides: int
@export var value: int
func _init(face_count: int = 6, face: int = 1) -> void:
\tsides = face_count
\tvalue = face
''',
        "action_log_message.gd": f'''extends Resource

const ActionLogText = preload("{root}action_log_text.gd")
const ActionLogDie = preload("{root}action_log_die.gd")
@export var title: String
@export var text: Array[ActionLogText] = []
@export var dice: Array[ActionLogDie] = []
@export var result: String = ""
## info, success, attention, or roll. Meaning belongs to the caller.
@export var tone: String = "info"
func _init(heading: String = "") -> void:
\ttitle = heading
func to_record() -> Dictionary:
\tvar runs: Array = []
\tvar faces: Array = []
\tfor run in text:
\t\tif run == null:
\t\t\truns.append(null)
\t\telse:
\t\t\truns.append({{"text": run.text, "style": run.style}})
\tfor die in dice:
\t\tif die == null:
\t\t\tfaces.append(null)
\t\telse:
\t\t\tfaces.append({{"sides": die.sides, "value": die.value}})
\treturn {{"title": title, "text": runs, "dice": faces, "result": result, "tone": tone}}
''',
        "action_log_result.gd": f'''extends "{root}operation_result.gd"

var sequence: int = 0
func _init(outcome: Dictionary) -> void:
\tsuper(outcome)
\tif ok:
\t\tsequence = outcome.value.sequence
''',
        "action_log.gd": f'''extends RefCounted

const ActionLogMessage = preload("{root}action_log_message.gd")
const ActionLogResult = preload("{root}action_log_result.gd")
const WorldCapability = preload("{root}world_capability.gd")
var _host: Object
func _init(host: Object) -> void:
\t_host = host
## Await authority acceptance and broadcast. The host supplies Participant and Package attribution.
func publish(message: ActionLogMessage) -> ActionLogResult:
\tvar record: Dictionary = {{}} if message == null else message.to_record()
\treturn ActionLogResult.new(await WorldCapability.new().complete(_host, _host.PublishActionLog(record)))
''',
    }
