extends Resource

## Visible sky brightness, 0..8. Does not change the quality budget.
@export var energy: float = 0.7

## Panorama yaw in degrees, -360..360.
@export var rotation_degrees: float = 17.188734

func to_record() -> Dictionary:
	var result: Dictionary = {}
	result["energy"] = energy
	result["rotationDegrees"] = rotation_degrees
	return result

func read_record(record: Dictionary) -> void:
	if record.has("energy"):
		energy = record["energy"]
	if record.has("rotationDegrees"):
		rotation_degrees = record["rotationDegrees"]
