extends "res://rookframe/sdk/operation_result.gd"

const PublicIdentity = preload("res://rookframe/sdk/public_identity.gd")
var items: Array[PublicIdentity] = []
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_values: Array = result.value
		for value in raw_values:
			items.append(PublicIdentity.new(value))
