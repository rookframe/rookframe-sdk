extends Resource

## Constant ambient RGB, each channel 0..1.
@export var color: Color = Color(0.72, 0.80, 0.88)

## Constant ambient energy, 0..8; independent of sky brightness.
@export var energy: float = 0.21

func to_record() -> Dictionary:
	var result: Dictionary = {}
	result["color"] = {"r": color.r, "g": color.g, "b": color.b}
	result["energy"] = energy
	return result

func read_record(record: Dictionary) -> void:
	if record.has("color"):
		var color_record: Dictionary = record["color"]
		color = Color(float(color_record.r), float(color_record.g), float(color_record.b))
	if record.has("energy"):
		energy = record["energy"]
