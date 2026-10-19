extends "res://rookframe/sdk/operation_result.gd"

const SystemRecord = preload("res://rookframe/sdk/system_record.gd")
var system_record: SystemRecord
func _init(result: Dictionary) -> void:
	super(result)
	if ok:
		var raw_value: Dictionary = result.value
		system_record = SystemRecord.new(raw_value)
