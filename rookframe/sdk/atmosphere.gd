extends RefCounted
const SceneId = preload("res://rookframe/sdk/scene_id.gd")
const SceneAtmosphere = preload("res://rookframe/sdk/scene_atmosphere.gd")
const AtmosphereOverride = preload("res://rookframe/sdk/atmosphere_override.gd")
const AtmosphereResult = preload("res://rookframe/sdk/atmosphere_result.gd")
const OperationResult = preload("res://rookframe/sdk/operation_result.gd")
const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")

var _host: Object
func _init(host: Object) -> void:
	_host = host

## Read shared Scene intent, excluding this Participant's transient effects.
func read(scene: SceneId) -> AtmosphereResult:
	return AtmosphereResult.new(_host.ReadSceneAtmosphere(scene.value if scene != null else ""))

## GM-only durable change, automatically shared with every Participant.
## Use for weather/time-of-day milestones, not a per-frame animation loop.
## Success is final only after persistence. Existing state survives invalid input.
func set_scene(scene: SceneId, picture: SceneAtmosphere) -> OperationResult:
	return OperationResult.new(await WorldCapability.new().complete(_host, _host.SetSceneAtmosphere(
		scene.value if scene != null else "", picture.to_record() if picture != null else {})))

## Participant-local effect for one Scene; never changes World data or quality.
## The same Package/id replaces its prior effect. Supplied groups replace whole groups.
## Higher priority wins; equal priorities sort by Package UUID then effect ID.
## 32 effects per Package, ID 1..80 characters, priority -1000..1000.
## Stop/World exit removes all this Package's effects automatically.
func set_local(id: String, scene: SceneId, effect: AtmosphereOverride, priority: int = 0) -> OperationResult:
	return OperationResult.new(_host.SetLocalAtmosphere(id, scene.value if scene != null else "", priority,
		effect.to_record() if effect != null else {}))

## Idempotent. Removes only the calling Package's effect and reveals underlying intent.
func clear_local(id: String) -> OperationResult:
	return OperationResult.new(_host.ClearLocalAtmosphere(id))
