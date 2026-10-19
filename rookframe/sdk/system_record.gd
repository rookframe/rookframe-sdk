extends RefCounted

const SystemRecordId = preload("res://rookframe/sdk/system_record_id.gd")
var id: SystemRecordId
var type_name: String
var data: Variant
func _init(value: Dictionary) -> void:
	id = SystemRecordId.new(value.id)
	type_name = value.type_name
	data = value.data
