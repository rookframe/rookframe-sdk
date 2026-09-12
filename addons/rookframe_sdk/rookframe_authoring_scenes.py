"""Small native scene scaffolds owned by the Publisher after initialization."""
import json


def presentation(package_id: str) -> str:
    root = f"res://rookframe/packages/{package_id}"
    return f'''extends Control

const SDK = preload("{root}/sdk/package_sdk_facade.gd")
const RAIL = preload("{root}/ui/rail.tscn")
const WINDOW = preload("{root}/ui/window.tscn")
var sdk: RefCounted
var _window: Control


func compose_presentation(host: Object) -> Control:
\tsdk = SDK.new()
\tsdk.bind(host)
\tvar rail := RAIL.instantiate() as Button
\trail.pressed.connect(_open_window)
\tif not sdk.mount_rail("left", rail):
\t\trail.free()
\treturn self


func _open_window() -> void:
\tif _window == null:
\t\t_window = WINDOW.instantiate() as Control
\tsdk.open_extension_surface(_window)
'''


def window_scene(name: str) -> str:
    return f'''[gd_scene load_steps=3 format=3]

[ext_resource type="Theme" path="res://rookframe/ui/theme/rookframe_theme.tres" id="theme"]
[ext_resource type="PackedScene" path="res://rookframe/ui/components/layout/section.tscn" id="section"]

[node name="PackageWindow" type="VBoxContainer"]
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
size_flags_horizontal = 3
theme = ExtResource("theme")

[node name="Introduction" parent="." instance=ExtResource("section")]
layout_mode = 2
title = {json.dumps(name)}
description = "An extension for your World."

[node name="Description" type="Label" parent="."]
layout_mode = 2
theme_type_variation = &"RookframeBody"
text = "Replace this content with your authored scene."
autowrap_mode = 2
'''


def rail_scene(name: str) -> str:
    return f'''[gd_scene load_steps=3 format=3]

[ext_resource type="Theme" path="res://rookframe/ui/theme/rookframe_theme.tres" id="theme"]
[ext_resource type="Texture2D" path="res://rookframe/ui/icons/document.svg" id="icon"]

[node name="PackageRailEntry" type="Button"]
custom_minimum_size = Vector2(50, 50)
layout_mode = 2
theme = ExtResource("theme")
theme_type_variation = &"RookframeShellControl"
theme_override_constants/icon_max_width = 21
icon = ExtResource("icon")
expand_icon = false
tooltip_text = {json.dumps(name)}
accessibility_name = {json.dumps("Open " + name)}
'''
