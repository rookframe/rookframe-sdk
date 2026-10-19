extends RefCounted
const DataResult = preload("res://rookframe/sdk/data_result.gd")
const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
const SystemActionContext = preload("res://rookframe/sdk/system_action_context.gd")
var _host: Object
func _init(host: Object) -> void:
	_host = host

## Sends an intent; authority derives every private statistic and consequence.
func submit(name: String, data: Variant) -> DataResult:
	return DataResult.new(await WorldCapability.new().complete(_host, _host.SubmitSystemIntent(name, data)))

## Used by the generated Implementation callback. Expires when it returns.
func context(token: String) -> SystemActionContext:
	return SystemActionContext.new(_host, token)
