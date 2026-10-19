extends RefCounted
const ServiceScope = preload("res://rookframe/sdk/service_scope.gd")
const IntegrationResult = preload("res://rookframe/sdk/integration_result.gd")
const TextResult = preload("res://rookframe/sdk/text_result.gd")

var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
	_scope = scope
func read_text() -> TextResult:
	return TextResult.new(_scope._host.ReadClipboard())
func write_text(text: String) -> IntegrationResult:
	return IntegrationResult.new(_scope._host.WriteClipboard(text))
