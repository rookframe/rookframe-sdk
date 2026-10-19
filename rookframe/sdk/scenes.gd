extends RefCounted

const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
const RookId = preload("res://rookframe/sdk/rook_id.gd")
const SceneResult = preload("res://rookframe/sdk/scene_result.gd")
const DistanceResult = preload("res://rookframe/sdk/distance_result.gd")

var _host: Object
func _init(host: Object) -> void:
	_host = host

func current() -> SceneResult:
	return SceneResult.new(_host.CurrentScene())
func distance(from: RookId, to: RookId) -> DistanceResult:
	return DistanceResult.new(_host.RookDistance(from.value, to.value))
