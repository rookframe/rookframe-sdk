"""Typed Package Settings descriptors, snapshots and Rookframe-owned edit drafts."""


def settings_sources(root: str, *, typed_lists: bool = False) -> dict[str, str]:
    sources = {
        "settings_scope.gd": '''extends RefCounted
enum Kind { USER, WORLD }
''',
        "setting.gd": '''extends Resource
enum Application { LIVE, RESTART_LOCAL, RESTART_WORLD }
## Stable Package-local name. Rookframe supplies the Package namespace.
## Application policy belongs to the containing setting; nested fields stay LIVE.
@export var key: String
@export var title: String
@export_multiline var description: String
@export var application: Application = Application.LIVE

''',
        "text_setting.gd": f'''extends "{root}setting.gd"
@export var default_value: String = ""
@export var choices: PackedStringArray = []
@export var minimum_length: int = 0
@export var maximum_length: int = 4096

''',
        "secret_setting.gd": f'''extends "{root}setting.gd"
## Values use the existing protected store and never enter an ordinary draft/copy.
''',
        "settings_registration.gd": f'''extends Resource
const Setting = preload("{root}setting.gd")
@export var user: Array[Setting] = []
@export var world: Array[Setting] = []

''',
        "settings_validation.gd": '''extends RefCounted
## Empty message accepts the candidate; a message rejects it without publishing.
var message: String
func _init(rejection: String = "") -> void:
\tmessage = rejection
''',
    }
    for name, value_type, default in (
        ("toggle", "bool", "false"),
        ("integer", "int", "0"),
        ("number", "float", "0.0"),
    ):
        fields = f"@export var default_value: {value_type} = {default}\n"
        if name != "toggle":
            fields += f"@export var minimum: {value_type} = -1000000\n@export var maximum: {value_type} = 1000000\n"
        sources[f"{name}_setting.gd"] = f'''extends "{root}setting.gd"
{fields}
'''
    sources["object_setting.gd"] = f'''extends "{root}setting.gd"
const Setting = preload("{root}setting.gd")
@export var properties: Array[Setting] = []
'''
    sources["array_setting.gd"] = f'''extends "{root}setting.gd"
const Setting = preload("{root}setting.gd")
@export var item: Setting
'''
    kinds = (("text", "TextSetting", "String", '""'), ("toggle", "ToggleSetting", "bool", "false"),
             ("integer", "IntegerSetting", "int", "0"), ("number", "NumberSetting", "float", "0.0"),
             ("object", "ObjectSetting", "Dictionary", "{}"), ("array", "ArraySetting", "Array", "[]"))
    values = 'extends RefCounted\n\n'
    for name, type_name, _, _ in kinds:
        values += f'const {type_name} = preload("{root}{name}_setting.gd")\n'
    values += '''
var _values: Dictionary
func _init(values: Dictionary = {}) -> void:
\t_values = values.duplicate(true)

func _copy() -> Dictionary:
\treturn _values.duplicate(true)
'''
    draft = f'extends "{root}settings_values.gd"\n'
    for name, type_name, value_type, default in kinds:
        expression = f'_values.get(setting.key, {default})'
        if value_type in ("Dictionary", "Array"):
            values += f'\nfunc {name}(setting: {type_name}) -> {value_type}:\n\tvar value: {value_type} = {expression}\n\treturn value.duplicate(true)\n'
        else:
            values += f'\nfunc {name}(setting: {type_name}) -> {value_type}:\n\treturn {expression}\n'
        value = 'value.duplicate(true)' if value_type in ("Dictionary", "Array") else 'value'
        draft += f'\nfunc set_{name}(setting: {type_name}, value: {value_type}) -> void:\n\t_values[setting.key] = {value}\n'
    if typed_lists:
        for name, type_name, element, packed, bounds in (
            ("text_list", "TextListSetting", "String", "PackedStringArray", '@export var minimum_length: int = 0\n@export var maximum_length: int = 4096'),
            ("integer_list", "IntegerListSetting", "int", "PackedInt64Array", '@export var minimum: int = -1000000\n@export var maximum: int = 1000000'),
        ):
            sources[f"{name}_setting.gd"] = f'''extends "{root}setting.gd"
@export var default_value: {packed} = []
@export var minimum_items: int = 0
@export var maximum_items: int = 256
{bounds}
'''
            list_type = type_name.removesuffix("Setting")
            sources[f"{name}.gd"] = f'''extends RefCounted
## A detached typed list. Mutations affect this draft helper only.
var _source: Array
var _added: Array = []
func _init(values: Array = []) -> void:
\t_source = values.duplicate(true)
func size() -> int:
\treturn _source.size() + _added.size()
func is_empty() -> bool:
\treturn size() == 0
func at(index: int) -> {element}:
\tvar value: {element} = _source[index] if index < _source.size() else _added[index - _source.size()]
\treturn value
func append(value: {element}) -> void:
\t_added.append(value)
func _copy() -> Array:
\tvar values: Array = []
\tfor index in range(size()):
\t\tvalues.append(at(index))
\treturn values
'''
            values = values.replace("var _values: Dictionary", f'const {list_type} = preload("{root}{name}.gd")\nvar _values: Dictionary')
            values = values.replace("var _values: Dictionary", f'const {type_name} = preload("{root}{name}_setting.gd")\nvar _values: Dictionary')
            values += f'\nfunc {name}(setting: {type_name}) -> {list_type}:\n\treturn {list_type}.new(_values.get(setting.key, []))\n'
            draft += f'\nfunc set_{name}(setting: {type_name}, value: {list_type}) -> void:\n\t_values[setting.key] = value._copy()\n'
    sources["settings_values.gd"] = values
    sources["settings_draft.gd"] = draft
    sources["settings_candidate.gd"] = f'''extends "{root}settings_values.gd"
const SettingsScope = preload("{root}settings_scope.gd")
var scope: SettingsScope.Kind
func _init(candidate_scope: SettingsScope.Kind, values: Dictionary) -> void:
\tsuper(values)
\tscope = candidate_scope
'''
    sources["settings_migration.gd"] = f'''extends "{root}settings_draft.gd"
const SettingsScope = preload("{root}settings_scope.gd")
var scope: SettingsScope.Kind
var source_version: String
var target_version: String
func _init(candidate_scope: SettingsScope.Kind, source: String, target: String, values: Dictionary) -> void:
\tsuper(values)
\tscope = candidate_scope
\tsource_version = source
\ttarget_version = target
'''
    sources["settings.gd"] = f'''extends RefCounted
const SettingsScope = preload("{root}settings_scope.gd")
const SettingsValues = preload("{root}settings_values.gd")
## Only the owning Package receives accepted-change notifications.
signal changed(scope: SettingsScope.Kind)
var _host: Object
func _init(host: Object) -> void:
\t_host = host
\t_host.connect("SettingsChanged", _changed)

func _changed(scope: int) -> void:
\tchanged.emit(scope)

var user: SettingsValues:
\tget:
\t\treturn SettingsValues.new(_host.ReadPackageSettings(SettingsScope.Kind.USER, ""))
var world: SettingsValues:
\tget:
\t\treturn SettingsValues.new(_host.ReadPackageSettings(SettingsScope.Kind.WORLD, ""))

## Read an Enabled Package's non-secret copy. No registration or service object is shared.
func read_other(package_id: String, scope: SettingsScope.Kind) -> SettingsValues:
\treturn SettingsValues.new(_host.ReadPackageSettings(scope, package_id))
'''
    sources["settings_view.gd"] = f'''extends Control
const SettingsScope = preload("{root}settings_scope.gd")
const SettingsDraft = preload("{root}settings_draft.gd")
## The containing menu owns save/cancel, authorization, validation and persistence.
var draft: SettingsDraft = SettingsDraft.new()
var scope: SettingsScope.Kind

func _rookframe_edit_settings(edit_scope: int, values: Dictionary) -> void:
\tscope = edit_scope
\tdraft = SettingsDraft.new(values)
\tedit()

func _rookframe_settings_values() -> Dictionary:
\treturn draft._copy()

## Override to populate the authored form from this scope's draft.
func edit() -> void:
\tpass
'''
    sources["settings_view_definition.gd"] = '''extends Resource
## Authored Control with the SDK SettingsView base script.
@export var scene: PackedScene
'''
    return {name: source.rstrip() + "\n" for name, source in sources.items()}


def implementation_callbacks() -> str:
    return '''

## Override with fixed, typed definitions assembled from authored Setting resources.
func describe_settings() -> SDK.SettingsRegistration:
\treturn SDK.SettingsRegistration.new()

## Inspect the complete staged scope. Do not perform World operations here.
func validate_settings(candidate: SDK.SettingsCandidate) -> SDK.SettingsValidation:
\treturn SDK.SettingsValidation.new()

## Called once for a new exact version, only when an older copy exists.
func migrate_settings(migration: SDK.SettingsMigration) -> SDK.SettingsValues:
\treturn migration

func _rookframe_settings_schema() -> Dictionary:
\treturn get_meta("rookframe_sdk").DescribeSettings(describe_settings())

func _rookframe_validate_settings(scope: int, values: Dictionary) -> String:
\treturn validate_settings(SDK.SettingsCandidate.new(scope, values)).message

func _rookframe_migrate_settings(scope: int, source: String, target: String, values: Dictionary) -> Dictionary:
\treturn migrate_settings(SDK.SettingsMigration.new(scope, source, target, values))._copy()
'''
