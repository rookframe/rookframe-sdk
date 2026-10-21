extends RefCounted

const HudContribution = preload("res://rookframe/sdk/hud_contribution.gd")
var _host: Object

func _init(host: Object) -> void:
	_host = host

## System → Rookframe → Optional. Optional providers use World Package Selection
## order (canonical Package UUID); each provider then uses order and stable id.
func register(entry: HudContribution) -> void:
	_host.RegisterHud(entry.scene, entry.definition())
