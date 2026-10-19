extends "res://rookframe/sdk/integration_result.gd"
const ProviderTokens = preload("res://rookframe/sdk/provider_tokens.gd")

var found: bool
var tokens: ProviderTokens
func _init(result: Dictionary) -> void:
	super(result)
	found = result.get("found", false)
	if ok and found:
		tokens = ProviderTokens.new(result)
