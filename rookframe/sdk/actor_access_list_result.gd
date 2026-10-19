extends "res://rookframe/sdk/operation_result.gd"

const ActorAccessEntry = preload("res://rookframe/sdk/actor_access_entry.gd")

var items: Array[ActorAccessEntry] = []
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var rows: Array = result.value
		for value in rows:
			items.append(ActorAccessEntry.new(value))
