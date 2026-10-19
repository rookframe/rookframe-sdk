extends RefCounted

const RookId = preload("res://rookframe/sdk/rook_id.gd")
const ActorId = preload("res://rookframe/sdk/actor_id.gd")
const SceneId = preload("res://rookframe/sdk/scene_id.gd")
const ContentReference = preload("res://rookframe/sdk/content_reference.gd")
var id: RookId
var actor: ActorId
var scene: SceneId
var position: Vector2
var yaw: float
var miniature: ContentReference
var hidden: bool
func _init(value: Dictionary) -> void:
	var raw_miniature: Dictionary = value.miniature
	id = RookId.new(value.id)
	actor = ActorId.new(value.actor) if value.actor != "" else null
	scene = SceneId.new(value.scene)
	position = value.position
	yaw = value.yaw
	miniature = ContentReference.new(raw_miniature.packageId, raw_miniature.localId)
	hidden = value.hidden
