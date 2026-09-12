"""Small native scene scaffolds owned by the Publisher after initialization."""
import json


def presentation(package_id: str) -> str:
    root = f"res://rookframe/packages/{package_id}"
    return f'''extends "{root}/sdk/presentation.gd"

const WINDOW_BUTTON: SDK.WindowButton = preload("{root}/ui/window_button.tres")


func compose() -> void:
\tvar rail: SDK.Rail = sdk.rails.left
\trail.push(WINDOW_BUTTON)
'''


def window_button(package_id: str) -> str:
    root = f"res://rookframe/packages/{package_id}"
    return f'''[gd_resource type="Resource" load_steps=6 format=3]

[ext_resource type="Script" path="{root}/sdk/window_button.gd" id="entry"]
[ext_resource type="Script" path="{root}/sdk/extension_surface.gd" id="surface"]
[ext_resource type="PackedScene" path="{root}/ui/window_button.tscn" id="button"]
[ext_resource type="PackedScene" path="{root}/ui/window.tscn" id="window"]

[sub_resource type="Resource" id="ExtensionWindow"]
script = ExtResource("surface")
scene = ExtResource("window")

[resource]
script = ExtResource("entry")
button_scene = ExtResource("button")
window = SubResource("ExtensionWindow")
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
