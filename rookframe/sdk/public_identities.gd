extends RefCounted

const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
const ActorId = preload("res://rookframe/sdk/actor_id.gd")
const RookId = preload("res://rookframe/sdk/rook_id.gd")
const PublicIdentityResult = preload("res://rookframe/sdk/public_identity_result.gd")
const PublicIdentityListResult = preload("res://rookframe/sdk/public_identity_list_result.gd")
const OperationResult = preload("res://rookframe/sdk/operation_result.gd")

var _host: Object
func _init(host: Object) -> void:
	_host = host

func list() -> PublicIdentityListResult:
	return PublicIdentityListResult.new(_host.ListPublicIdentities())
func read(rook: RookId) -> PublicIdentityResult:
	return PublicIdentityResult.new(_host.ReadPublicIdentity(rook.value))
func assign(actor: ActorId, label: String) -> OperationResult:
	return OperationResult.new(await WorldCapability.new().complete(_host, _host.SetPublicIdentity(actor.value, label)))
