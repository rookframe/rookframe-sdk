extends Resource

## Degrees, -90..90. Negative points sunlight downwards.
@export var pitch_degrees: float = -38.0

## World yaw in degrees, -360..360.
@export var yaw_degrees: float = -58.0

## Sun RGB, each channel 0..1; alpha is unused.
@export var color: Color = Color(1.0, 0.84, 0.60)

## Direct light energy, 0..16. Zero makes the sun dark.
@export var energy: float = 3.6

func to_record() -> Dictionary:
	var result: Dictionary = {}
	result["pitchDegrees"] = pitch_degrees
	result["yawDegrees"] = yaw_degrees
	result["color"] = {"r": color.r, "g": color.g, "b": color.b}
	result["energy"] = energy
	return result

func read_record(record: Dictionary) -> void:
	if record.has("pitchDegrees"):
		pitch_degrees = record["pitchDegrees"]
	if record.has("yawDegrees"):
		yaw_degrees = record["yawDegrees"]
	if record.has("color"):
		var color_record: Dictionary = record["color"]
		color = Color(float(color_record.r), float(color_record.g), float(color_record.b))
	if record.has("energy"):
		energy = record["energy"]
