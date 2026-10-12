"""Edition 2029 revision 33: explicit transient announcements, separate from history."""


def announcement_sources(root: str) -> dict[str, str]:
    return {
        "announcement.gd": '''extends Resource

## Two compact text lines; the host handles truncation and responsive layout.
@export var subject: String
@export var caption: String
## info, dice, attack, power, item, recovery. Uses the host's themed icons.
@export var icon: String = "info"
## Numeric dice results only; never success/failure labels.
@export var results: Array[int] = []
## Optional accepted Action Log sequence. Zero opens history without a linked record.
@export var log_sequence: int = 0
func _init(who: String = "", what: String = "", symbol: String = "info") -> void:
\tsubject = who
\tcaption = what
\ticon = symbol
func to_record() -> Dictionary:
\treturn {"subject": subject, "caption": caption, "icon": icon, "results": results, "logSequence": log_sequence}
''',
        "announcements.gd": f'''extends RefCounted
const Announcement = preload("{root}announcement.gd")
const OperationResult = preload("{root}operation_result.gd")
const WorldCapability = preload("{root}world_capability.gd")
var _host: Object
func _init(host: Object) -> void:
\t_host = host
## Broadcast to currently connected Participants after authority acceptance.
## Does not write history, replay on reconnect, or interpret System outcomes.
func announce(message: Announcement) -> OperationResult:
\tvar record: Dictionary = {{}} if message == null else message.to_record()
\treturn OperationResult.new(await WorldCapability.new().complete(_host, _host.Announce(record)))
''',
    }


def extend_reporting(sources: dict[str, str], root: str) -> None:
    sources["action_log.gd"] += '''
## Record richer history without changing the tabletop announcement.
## Await acceptance before using the returned sequence as an announcement link.
func write(message: ActionLogMessage) -> ActionLogResult:
\treturn await publish(message)
'''
    sources["action_log_result.gd"] = sources["action_log_result.gd"].replace(
        'sequence = outcome.value.sequence', 'sequence = outcome.value.get("sequence", 0)')
    context = sources["system_action_context.gd"]
    context = context.replace(' -> OperationResult:', ' -> ActionLogResult:').replace(
        'return OperationResult.new(_host.SystemIntentCommit', 'return ActionLogResult.new(_host.SystemIntentCommit')
    context += f'''
const ActionLogResult = preload("{root}action_log_result.gd")
const Announcement = preload("{root}announcement.gd")
## Write with the authenticated intent caller's attribution. No Actor changes.
func write_action_log(message: ActionLogMessage) -> ActionLogResult:
\treturn commit([], message)
## Explicit shared presentation after an accepted commit. Does not write history.
func announce(message: Announcement) -> OperationResult:
\treturn OperationResult.new(_host.SystemIntentAnnounce(_token, message.to_record() if message != null else {{}}))
'''
    sources["system_action_context.gd"] = context
