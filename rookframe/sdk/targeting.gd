extends RefCounted

const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
const TargetSnapshot = preload("res://rookframe/sdk/target_snapshot.gd")
const TargetSnapshotResult = preload("res://rookframe/sdk/target_snapshot_result.gd")

var _host: Object
func _init(host: Object) -> void:
	_host = host
	_host.TargetingChanged.connect(_changed)

signal changed(snapshot: TargetSnapshot)
func _changed(outcome: Dictionary) -> void:
	changed.emit(TargetSnapshot.new(outcome.value))
func snapshot() -> TargetSnapshotResult:
	return TargetSnapshotResult.new(await WorldCapability.new().complete(_host, _host.TargetingSnapshot()))

const OperationResult = preload("res://rookframe/sdk/operation_result.gd")

## Temporarily reveal the tabletop; Done restores window placement and focus.
func choose() -> OperationResult:
	return OperationResult.new(_host.ChooseTargets())

const RookId = preload("res://rookframe/sdk/rook_id.gd")
## Show an animated range around a Rook and constrain local picking to one target.
## The action window remains visible. Existing targets are retained for validation.
func begin_range(source: RookId, metres: float, caption: String = "") -> OperationResult:
	return OperationResult.new(_host.BeginLabeledTargetRange(source.value if source != null else "", metres, caption))
func end_range() -> OperationResult:
	return OperationResult.new(_host.EndTargetRange())
