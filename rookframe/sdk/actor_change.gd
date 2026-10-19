extends RefCounted
const ActorId = preload("res://rookframe/sdk/actor_id.gd")
var actor: ActorId
var data: Variant
func _init(identity: ActorId, replacement: Variant) -> void:
	actor = identity
	data = replacement
func to_record() -> Dictionary:
	return {"id": actor.value, "data": data}
