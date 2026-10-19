extends RefCounted
const ServiceScope = preload("res://rookframe/sdk/service_scope.gd")
const IntegrationResult = preload("res://rookframe/sdk/integration_result.gd")

var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
	_scope = scope
func open(url: String) -> IntegrationResult:
	return IntegrationResult.new(await _scope._complete(_scope._host.OpenBrowserLink(url)))
