extends RefCounted
const Announcement = preload("res://rookframe/sdk/announcement.gd")
const OperationResult = preload("res://rookframe/sdk/operation_result.gd")
const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
var _host: Object
func _init(host: Object) -> void:
	_host = host
## Broadcast to currently connected Participants after authority acceptance.
## Does not write history, replay on reconnect, or interpret System outcomes.
func announce(message: Announcement) -> OperationResult:
	var record: Dictionary = {} if message == null else message.to_record()
	return OperationResult.new(await WorldCapability.new().complete(_host, _host.Announce(record)))
