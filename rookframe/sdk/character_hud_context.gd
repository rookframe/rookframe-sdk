extends "res://rookframe/sdk/operation_result.gd"
const ActorId = preload("res://rookframe/sdk/actor_id.gd")
const RookId = preload("res://rookframe/sdk/rook_id.gd")
## Null Actor means there is no owned character context. Selection is never changed.
var actor: ActorId
var rook: RookId
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var value: Dictionary = result.value
		actor = ActorId.new(value.actor_id) if not str(value.actor_id).is_empty() else null
		rook = RookId.new(value.rook_id) if not str(value.rook_id).is_empty() else null
