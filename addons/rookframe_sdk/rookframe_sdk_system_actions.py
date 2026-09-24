"""Edition 2029 revision 12: authority-side System intent and consequence boundary."""


def system_action_sources(root: str, *, participant_sessions: bool = False) -> dict[str, str]:
    sources = {
        "system_actions.gd": f'''extends RefCounted
const DataResult = preload("{root}data_result.gd")
const WorldCapability = preload("{root}world_capability.gd")
const SystemActionContext = preload("{root}system_action_context.gd")
var _host: Object
func _init(host: Object) -> void:
\t_host = host

## Sends an intent; authority derives every private statistic and consequence.
func submit(name: String, data: Variant) -> DataResult:
\treturn DataResult.new(await WorldCapability.new().complete(_host, _host.SubmitSystemIntent(name, data)))

## Used by the generated Implementation callback. Expires when it returns.
func context(token: String) -> SystemActionContext:
\treturn SystemActionContext.new(_host, token)
''',
        "actor_change.gd": f'''extends RefCounted
const ActorId = preload("{root}actor_id.gd")
var actor: ActorId
var data: Variant
func _init(identity: ActorId, replacement: Variant) -> void:
\tactor = identity
\tdata = replacement
func to_record() -> Dictionary:
\treturn {{"id": actor.value, "data": data}}
''',
        "system_action_context.gd": f'''extends RefCounted
const DataResult = preload("{root}data_result.gd")
const ActorId = preload("{root}actor_id.gd")
const ActorResult = preload("{root}actor_result.gd")
const RookId = preload("{root}rook_id.gd")
const RookResult = preload("{root}rook_result.gd")
const DistanceResult = preload("{root}distance_result.gd")
const ActorAccessListResult = preload("{root}actor_access_list_result.gd")
const HumanThrowRequest = preload("{root}human_throw_request.gd")
const HumanThrowResult = preload("{root}human_throw_result.gd")
const ActorChange = preload("{root}actor_change.gd")
const ActionLogMessage = preload("{root}action_log_message.gd")
const OperationResult = preload("{root}operation_result.gd")
var _host: Object
var _token: String
func _init(host: Object, token: String) -> void:
\t_host = host
\t_token = token

func new_request_id() -> String:
\treturn _host.NewHumanThrowRequestId()

## Authenticated requester, session and shared target Rooks. Never client assertions.
func caller() -> DataResult:
\treturn DataResult.new(_host.SystemIntentContext(_token))
## Complete shared Actor state. access_level describes the requesting Participant.
func read_actor(actor: ActorId) -> ActorResult:
\treturn ActorResult.new(_host.SystemIntentReadActor(_token, actor.value))
func read_rook(rook: RookId) -> RookResult:
\treturn RookResult.new(_host.SystemIntentReadRook(_token, rook.value))
func actor_access(actor: ActorId) -> ActorAccessListResult:
\treturn ActorAccessListResult.new(_host.SystemIntentActorAccess(_token, actor.value))
## Committed logical centers. One tabletop unit is one metre.
func distance(from: RookId, to: RookId) -> DistanceResult:
\treturn DistanceResult.new(_host.SystemIntentDistance(_token, from.value, to.value))
func read_throw(id: String) -> HumanThrowResult:
\treturn HumanThrowResult.new(_host.SystemIntentReadThrow(_token, id))
func request_throw(request: HumanThrowRequest) -> HumanThrowResult:
\treturn HumanThrowResult.new(_host.SystemIntentRequestThrow(_token, request.request_id, request.participant_id, request.to_records()))
func cancel_throw(id: String) -> HumanThrowResult:
\treturn HumanThrowResult.new(_host.SystemIntentCancelThrow(_token, id))
## Validates every replacement before saving the complete batch. No access grants.
## The System owns rule validation and must deliberately author a public report.
func commit(changes: Array[ActorChange], report: ActionLogMessage = null) -> OperationResult:
\tvar records: Array = []
\tfor change in changes:
\t\trecords.append(change.to_record())
\treturn OperationResult.new(_host.SystemIntentCommit(_token, records, report.to_record() if report != null else {{}}))
''',
    }
    if participant_sessions:
        sources["system_action_context.gd"] += '''
## Live Participant sessions, including the GM only when connected.
## Compare exact session identities; reconnect never continues an old action.
func participant_sessions() -> DataResult:
\treturn DataResult.new(_host.SystemIntentParticipantSessions(_token))
'''
    return sources
