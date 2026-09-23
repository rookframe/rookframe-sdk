"""Edition 2029 revisions 6–7: immediate and requested physical Throws."""


def dice_sources(root: str, *, requested_throws: bool = False) -> dict[str, str]:
    sources = {
        "dice_term.gd": '''extends Resource

## Package-owned name for one raw pool term. Rookframe does not interpret it.
@export var name: String
@export var faces: int
@export var count: int = 1
func _init(term_name: String = "", face_count: int = 6, dice_count: int = 1) -> void:
\tname = term_name
\tfaces = face_count
\tcount = dice_count
func to_record() -> Dictionary:
\treturn {"name": name, "faces": faces, "count": count}
''',
        "dice_request.gd": f'''extends Resource

const DiceTerm = preload("{root}dice_term.gd")
## Terms retain this order. Their total count may not exceed sixteen dice.
@export var terms: Array[DiceTerm] = []
func _init(requested_terms: Array[DiceTerm] = []) -> void:
\tterms = requested_terms
func to_records() -> Array:
\tvar records: Array = []
\tfor term in terms:
\t\trecords.append({{}} if term == null else term.to_record())
\treturn records
''',
        "dice_term_result.gd": '''extends RefCounted

## The caller-supplied name and raw physical faces/results, without game meaning.
var name: String
var faces: int
var results: Array[int] = []
func _init(value: Dictionary) -> void:
\tname = value.get("name", "")
\tfaces = value.get("faces", 0)
\tfor result in value.get("results", []):
\t\tresults.append(result)
''',
        "dice_roll_result.gd": f'''extends "{root}operation_result.gd"

const DiceTermResult = preload("{root}dice_term_result.gd")
var terms: Array[DiceTermResult] = []
## Sequence of Rookframe's built-in raw Roll report in the shared Action Log.
var sequence: int = 0
func _init(result: Dictionary) -> void:
\tsuper(result)
\tif ok:
\t\tvar value: Dictionary = result.get("value", {})
\t\tfor term in value.get("terms", []):
\t\t\tterms.append(DiceTermResult.new(term))
\t\tsequence = value.get("sequence", 0)
''',
        "dice.gd": f'''extends RefCounted

const DiceRequest = preload("{root}dice_request.gd")
const DiceRollResult = preload("{root}dice_roll_result.gd")
const WorldCapability = preload("{root}world_capability.gd")
var _host: Object
func _init(host: Object) -> void:
\t_host = host
## Allocate a stable UUID before persisting a requested action.
func new_request_id() -> String:
\treturn _host.NewHumanThrowRequestId()
## Physically roll now and await the committed raw named result.
func roll(request: DiceRequest) -> DiceRollResult:
\tvar terms: Array = [] if request == null else request.to_records()
\treturn DiceRollResult.new(await WorldCapability.new().complete(_host, _host.RollDice(terms)))
''',
    }
    if requested_throws:
        sources.update({
            "human_throw_request.gd": f'''extends Resource

const DiceTerm = preload("{root}dice_term.gd")
## Stable Package-owned UUID. Retrying it recovers the same immutable request.
@export var request_id: String
## Stable World Participant identity that must perform the physical Throw.
@export var participant_id: String
@export var terms: Array[DiceTerm] = []
func _init(identity: String = "", participant: String = "", requested_terms: Array[DiceTerm] = []) -> void:
\trequest_id = identity
\tparticipant_id = participant
\tterms = requested_terms
func to_records() -> Array:
\tvar records: Array = []
\tfor term in terms:
\t\trecords.append({{}} if term == null else term.to_record())
\treturn records
''',
            "human_throw_result.gd": f'''extends "{root}operation_result.gd"

const DiceTerm = preload("{root}dice_term.gd")
const DiceTermResult = preload("{root}dice_term_result.gd")
var request_id: String
var participant_id: String
## One of pending, rolled, or cancelled.
var status: String
## Immutable requested terms, available in every successful snapshot.
var plan: Array[DiceTerm] = []
## Raw named results when status is rolled; otherwise empty.
var terms: Array[DiceTermResult] = []
## Sequence of Rookframe's built-in raw Roll report, or zero before a Roll.
var sequence: int = 0
func _init(result: Dictionary) -> void:
\tsuper(result)
\tif ok:
\t\tvar value: Dictionary = result.get("value", {})
\t\trequest_id = value.get("request_id", "")
\t\tparticipant_id = value.get("participant_id", "")
\t\tstatus = value.get("status", "")
\t\tfor term in value.get("plan", []):
\t\t\tplan.append(DiceTerm.new(term.get("name", ""), term.get("faces", 0), term.get("count", 0)))
\t\tfor term in value.get("terms", []):
\t\t\tterms.append(DiceTermResult.new(term))
\t\tsequence = value.get("sequence", 0)
''',
        })
        sources["dice.gd"] = sources["dice.gd"].replace(
            f'const DiceRollResult = preload("{root}dice_roll_result.gd")',
            f'''const DiceRollResult = preload("{root}dice_roll_result.gd")
const HumanThrowRequest = preload("{root}human_throw_request.gd")
const HumanThrowResult = preload("{root}human_throw_result.gd")''') + '''
## Create or recover one durable request snapshot. This call never remains
## suspended while a human acts; retry request_id after sdk.world_changed.
func request_throw(request: HumanThrowRequest) -> HumanThrowResult:
\tif request == null:
\t\treturn HumanThrowResult.new(await WorldCapability.new().complete(_host, _host.RequestHumanThrow("", "", [])))
\treturn HumanThrowResult.new(await WorldCapability.new().complete(_host, _host.RequestHumanThrow(
\t\trequest.request_id, request.participant_id, request.to_records())))
'''
    return sources
