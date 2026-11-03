extends Resource
const AtmosphereSun = preload("res://rookframe/sdk/atmosphere_sun.gd")
const AtmosphereAmbient = preload("res://rookframe/sdk/atmosphere_ambient.gd")
const AtmosphereSky = preload("res://rookframe/sdk/atmosphere_sky.gd")
const AtmosphereFog = preload("res://rookframe/sdk/atmosphere_fog.gd")
const AtmosphereGrade = preload("res://rookframe/sdk/atmosphere_grade.gd")
const AtmosphereOcclusion = preload("res://rookframe/sdk/atmosphere_occlusion.gd")

## Required artistic group; no device settings.
@export var sun: AtmosphereSun = AtmosphereSun.new()

## Required artistic group; no device settings.
@export var ambient: AtmosphereAmbient = AtmosphereAmbient.new()

## Required artistic group; no device settings.
@export var sky: AtmosphereSky = AtmosphereSky.new()

## Required artistic group; no device settings.
@export var fog: AtmosphereFog = AtmosphereFog.new()

## Required artistic group; no device settings.
@export var grade: AtmosphereGrade = AtmosphereGrade.new()

## Required artistic group; no device settings.
@export var occlusion: AtmosphereOcclusion = AtmosphereOcclusion.new()

func to_record() -> Dictionary:
	var result: Dictionary = {}
	if sun != null:
		result["sun"] = sun.to_record()
	if ambient != null:
		result["ambient"] = ambient.to_record()
	if sky != null:
		result["sky"] = sky.to_record()
	if fog != null:
		result["fog"] = fog.to_record()
	if grade != null:
		result["grade"] = grade.to_record()
	if occlusion != null:
		result["occlusion"] = occlusion.to_record()
	return result

func read_record(record: Dictionary) -> void:
	if record.has("sun"):
		sun = AtmosphereSun.new()
		sun.read_record(record["sun"])
	if record.has("ambient"):
		ambient = AtmosphereAmbient.new()
		ambient.read_record(record["ambient"])
	if record.has("sky"):
		sky = AtmosphereSky.new()
		sky.read_record(record["sky"])
	if record.has("fog"):
		fog = AtmosphereFog.new()
		fog.read_record(record["fog"])
	if record.has("grade"):
		grade = AtmosphereGrade.new()
		grade.read_record(record["grade"])
	if record.has("occlusion"):
		occlusion = AtmosphereOcclusion.new()
		occlusion.read_record(record["occlusion"])
