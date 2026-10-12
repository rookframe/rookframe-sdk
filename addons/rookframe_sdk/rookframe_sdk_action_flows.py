"""Edition 2029 revision 34: updateable records and linked requested Throws."""


def extend_action_flows(sources: dict[str, str]) -> None:
    sources["action_log.gd"] += '''
## Append a step to the same record. Its identity and original attribution stay fixed.
func update(sequence: int, message: ActionLogMessage) -> ActionLogResult:
	return ActionLogResult.new(await WorldCapability.new().complete(_host, _host.UpdateActionLog(sequence, message.to_record())))
'''
    sources["human_throw_request.gd"] += '''
## Attach the physical Roll to this record instead of publishing a separate row.
@export var log_sequence: int = 0
'''
    context = sources["system_action_context.gd"]
    context = context.replace(
        'func request_throw(request: HumanThrowRequest) -> HumanThrowResult:\n',
        '''func request_throw(request: HumanThrowRequest) -> HumanThrowResult:
	if request.log_sequence > 0:
		return HumanThrowResult.new(_host.SystemIntentRequestLoggedThrow(_token, request.request_id, request.participant_id, request.to_records(), request.base_modifier, request.allow_modifier, request.log_sequence))
''')
    context = context.replace(
        'func commit(changes: Array[ActorChange], report: ActionLogMessage = null)',
        'func commit(changes: Array[ActorChange], report: ActionLogMessage = null, log_sequence: int = 0)')
    context = context.replace(
        '\treturn ActionLogResult.new(_host.SystemIntentCommit(_token, records,',
        '''	if log_sequence > 0:
		return ActionLogResult.new(_host.SystemIntentCommitLog(_token, records, report.to_record() if report != null else {}, log_sequence))
	return ActionLogResult.new(_host.SystemIntentCommit(_token, records,''')
    context += '''
## Append an accepted step; the host retains previous steps and linked raw Rolls.
func update_action_log(sequence: int, message: ActionLogMessage) -> ActionLogResult:
	return commit([], message, sequence)
'''
    sources["system_action_context.gd"] = context
