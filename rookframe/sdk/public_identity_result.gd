extends "res://rookframe/sdk/operation_result.gd"

const PublicIdentity = preload("res://rookframe/sdk/public_identity.gd")
var public_identity: PublicIdentity
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_value: Dictionary = result.value
		public_identity = PublicIdentity.new(raw_value)
