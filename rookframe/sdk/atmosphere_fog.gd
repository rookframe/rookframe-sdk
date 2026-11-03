extends Resource

## Depth fog opacity, 0..1. Zero clears fog; not a performance setting.
@export var density: float = 0.33

## Fog RGB, each channel 0..1.
@export var color: Color = Color(0.45, 0.57, 0.61)

## Fog light energy, 0..8.
@export var energy: float = 1.0

## Start distance in metres, 0..100000; must precede end.
@export var begin: float = 18.0

## End distance in metres, 0.01..100000; must follow begin.
@export var end: float = 105.0

## Depth distribution exponent, 0.01..16.
@export var curve: float = 1.25

## Influence on the sky, 0..1.
@export var sky_affect: float = 0.03

## Height reference in world metres, -100000..100000.
@export var height: float = 0.0

## Height contribution, -16..16. Zero disables it.
@export var height_density: float = 0.0

## Sunlight scattering, 0..1.
@export var sun_scatter: float = 0.08

## Blend toward the sky with distance, 0..1.
@export var aerial_perspective: float = 0.0

func to_record() -> Dictionary:
	var result: Dictionary = {}
	result["density"] = density
	result["color"] = {"r": color.r, "g": color.g, "b": color.b}
	result["energy"] = energy
	result["begin"] = begin
	result["end"] = end
	result["curve"] = curve
	result["skyAffect"] = sky_affect
	result["height"] = height
	result["heightDensity"] = height_density
	result["sunScatter"] = sun_scatter
	result["aerialPerspective"] = aerial_perspective
	return result

func read_record(record: Dictionary) -> void:
	if record.has("density"):
		density = record["density"]
	if record.has("color"):
		var color_record: Dictionary = record["color"]
		color = Color(float(color_record.r), float(color_record.g), float(color_record.b))
	if record.has("energy"):
		energy = record["energy"]
	if record.has("begin"):
		begin = record["begin"]
	if record.has("end"):
		end = record["end"]
	if record.has("curve"):
		curve = record["curve"]
	if record.has("skyAffect"):
		sky_affect = record["skyAffect"]
	if record.has("height"):
		height = record["height"]
	if record.has("heightDensity"):
		height_density = record["heightDensity"]
	if record.has("sunScatter"):
		sun_scatter = record["sunScatter"]
	if record.has("aerialPerspective"):
		aerial_perspective = record["aerialPerspective"]
