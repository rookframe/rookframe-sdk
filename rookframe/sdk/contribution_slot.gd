extends RefCounted

const Contribution = preload("res://rookframe/sdk/contribution.gd")
var _host: Object
var _slot: String

func _init(host: Object, slot: String) -> void:
	_host = host
	_slot = slot

## Append an authored contribution in Package-local order. Repeated scenes are idempotent.
func push(entry: Contribution) -> void:
	_host.RegisterContribution(_slot, entry.scene)
