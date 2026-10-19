extends "res://rookframe/sdk/integration_result.gd"
const ScopedStream = preload("res://rookframe/sdk/scoped_stream.gd")

var stream: ScopedStream
func _init(result: Dictionary, opened: ScopedStream) -> void:
	super(result)
	stream = opened
