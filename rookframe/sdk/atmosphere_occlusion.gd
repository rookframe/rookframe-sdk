extends Resource

## Contact shading radius in metres, 0.01..16.
@export var radius: float = 3.0

## Desired contact shading strength, 0..16; zero clears it.
@export var intensity: float = 2.0

## Contact shading response, 0.01..8.
@export var power: float = 1.3

## Small-scale contact shading strength, 0..5.
@export var detail: float = 1.5

## Influence on directly lit surfaces, 0..1.
@export var light_affect: float = 0.5

func to_record() -> Dictionary:
	var result: Dictionary = {}
	result["radius"] = radius
	result["intensity"] = intensity
	result["power"] = power
	result["detail"] = detail
	result["lightAffect"] = light_affect
	return result

func read_record(record: Dictionary) -> void:
	if record.has("radius"):
		radius = record["radius"]
	if record.has("intensity"):
		intensity = record["intensity"]
	if record.has("power"):
		power = record["power"]
	if record.has("detail"):
		detail = record["detail"]
	if record.has("lightAffect"):
		light_affect = record["lightAffect"]
