extends RefCounted

const TextSetting = preload("res://rookframe/sdk/text_setting.gd")
const ToggleSetting = preload("res://rookframe/sdk/toggle_setting.gd")
const IntegerSetting = preload("res://rookframe/sdk/integer_setting.gd")
const NumberSetting = preload("res://rookframe/sdk/number_setting.gd")
const ObjectSetting = preload("res://rookframe/sdk/object_setting.gd")
const ArraySetting = preload("res://rookframe/sdk/array_setting.gd")

const TextList = preload("res://rookframe/sdk/text_list.gd")
const TextListSetting = preload("res://rookframe/sdk/text_list_setting.gd")
const IntegerList = preload("res://rookframe/sdk/integer_list.gd")
const IntegerListSetting = preload("res://rookframe/sdk/integer_list_setting.gd")
var _values: Dictionary
func _init(values: Dictionary = {}) -> void:
	_values = values.duplicate(true)

func _copy() -> Dictionary:
	return _values.duplicate(true)

func text(setting: TextSetting) -> String:
	return _values.get(setting.key, "")

func toggle(setting: ToggleSetting) -> bool:
	return _values.get(setting.key, false)

func integer(setting: IntegerSetting) -> int:
	return _values.get(setting.key, 0)

func number(setting: NumberSetting) -> float:
	return _values.get(setting.key, 0.0)

func object(setting: ObjectSetting) -> Dictionary:
	var value: Dictionary = _values.get(setting.key, {})
	return value.duplicate(true)

func array(setting: ArraySetting) -> Array:
	var value: Array = _values.get(setting.key, [])
	return value.duplicate(true)

func text_list(setting: TextListSetting) -> TextList:
	return TextList.new(_values.get(setting.key, []))

func integer_list(setting: IntegerListSetting) -> IntegerList:
	return IntegerList.new(_values.get(setting.key, []))
