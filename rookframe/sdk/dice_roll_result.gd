extends "res://rookframe/sdk/operation_result.gd"

const DiceTermResult = preload("res://rookframe/sdk/dice_term_result.gd")
var terms: Array[DiceTermResult] = []
## Sequence of Rookframe's built-in raw Roll report in the shared Action Log.
var sequence: int = 0
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var value: Dictionary = result.get("value", {})
		for term in value.get("terms", []):
			terms.append(DiceTermResult.new(term))
		sequence = value.get("sequence", 0)
