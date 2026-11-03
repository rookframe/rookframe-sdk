extends Resource

## Owning Package UUID. Empty selects a Rookframe built-in.
@export var package_id: String = ""

## Package-relative cubic Texture3D (2..64, no mipmaps). Built-ins: "forest" or "" (neutral).
@export var path: String = "forest"

func to_record() -> Dictionary:
	var result: Dictionary = {}
	result["packageId"] = package_id
	result["path"] = path
	return result

func read_record(record: Dictionary) -> void:
	if record.has("packageId"):
		package_id = record["packageId"]
	if record.has("path"):
		path = record["path"]
