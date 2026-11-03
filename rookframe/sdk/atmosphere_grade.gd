extends Resource
const AtmosphereLookup = preload("res://rookframe/sdk/atmosphere_lookup.gd")

## AgX exposure, 0.01..16.
@export var exposure: float = 1.65

## AgX contrast, 0.1..2; no additional sampling cost.
@export var agx_contrast: float = 1.4

## AgX white, 1..64. Mobile uses its fixed white unless HDR 2D is enabled.
@export var agx_white: float = 16.29

## Post-tonemap brightness, 0..4.
@export var brightness: float = 1.0

## Post-tonemap contrast, 0..4.
@export var contrast: float = 1.0

## Post-tonemap saturation, 0..4; zero is monochrome.
@export var saturation: float = 0.95

## Immutable authored lookup. Preload changes; do not swap assets every frame.
@export var lookup: AtmosphereLookup = AtmosphereLookup.new()

func to_record() -> Dictionary:
	var result: Dictionary = {}
	result["exposure"] = exposure
	result["agxContrast"] = agx_contrast
	result["agxWhite"] = agx_white
	result["brightness"] = brightness
	result["contrast"] = contrast
	result["saturation"] = saturation
	if lookup != null:
		result["lookup"] = lookup.to_record()
	return result

func read_record(record: Dictionary) -> void:
	if record.has("exposure"):
		exposure = record["exposure"]
	if record.has("agxContrast"):
		agx_contrast = record["agxContrast"]
	if record.has("agxWhite"):
		agx_white = record["agxWhite"]
	if record.has("brightness"):
		brightness = record["brightness"]
	if record.has("contrast"):
		contrast = record["contrast"]
	if record.has("saturation"):
		saturation = record["saturation"]
	if record.has("lookup"):
		lookup = AtmosphereLookup.new()
		lookup.read_record(record["lookup"])
