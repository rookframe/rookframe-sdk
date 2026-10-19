extends RefCounted

const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
const OperationResult = preload("res://rookframe/sdk/operation_result.gd")

var _host: Object
func _init(host: Object) -> void:
	_host = host

var _capability: String
func configure(name: String) -> void:
	_capability = name
## Integration boundary reserved for the owning project; no predicted gameplay result.
func status() -> OperationResult:
	return OperationResult.new(_host.CapabilityStatus(_capability))
