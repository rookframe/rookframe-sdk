extends "res://rookframe/sdk/integration_result.gd"
enum State { UNAVAILABLE, SIGNED_OUT, SIGNED_IN, EXPIRED }
var state: State
func _init(result: Dictionary) -> void:
	super(result)
	state = result.get("state", State.UNAVAILABLE)
