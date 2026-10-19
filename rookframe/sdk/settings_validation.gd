extends RefCounted
## Empty message accepts the candidate; a message rejects it without publishing.
var message: String
func _init(rejection: String = "") -> void:
	message = rejection
