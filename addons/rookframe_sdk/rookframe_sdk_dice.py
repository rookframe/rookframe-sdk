"""Edition 2029 revision 6: named immediate physical dice requests."""


def dice_sources(root: str) -> dict[str, str]:
    return {
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
\t\tfor term in result.value.get("terms", []):
\t\t\tterms.append(DiceTermResult.new(term))
\t\tsequence = result.value.get("sequence", 0)
''',
        "dice.gd": f'''extends RefCounted

const DiceRequest = preload("{root}dice_request.gd")
const DiceRollResult = preload("{root}dice_roll_result.gd")
const WorldCapability = preload("{root}world_capability.gd")
var _host: Object
func _init(host: Object) -> void:
\t_host = host
## Physically roll now and await the committed raw named result.
func roll(request: DiceRequest) -> DiceRollResult:
\tvar terms: Array = [] if request == null else request.to_records()
\treturn DiceRollResult.new(await WorldCapability.new().complete(_host, _host.RollDice(terms)))
''',
    }
