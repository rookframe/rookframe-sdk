extends RefCounted
const ServiceScope = preload("res://rookframe/sdk/service_scope.gd")
const ServiceDefinition = preload("res://rookframe/sdk/service_definition.gd")
const NamedService = preload("res://rookframe/sdk/named_service.gd")
const Account = preload("res://rookframe/sdk/account.gd")

var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
	_scope = scope
func service(definition: ServiceDefinition, account: Account = null) -> NamedService:
	return NamedService.new(_scope, definition.name, account)
