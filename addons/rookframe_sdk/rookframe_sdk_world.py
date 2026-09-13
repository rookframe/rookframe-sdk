"""Concrete Package-scoped World capabilities and typed SDK-owned records."""
import re


def world_sources(root: str) -> dict[str, str]:
    def path(name):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + ".gd"

    def imports(*names):
        return "\n".join(f'const {name} = preload("{root}{path(name)}")' for name in names) + "\n"

    def capability(name, methods, types):
        return "extends RefCounted\n\n" + imports(*types) + '''
var _host: Object
func _init(host: Object) -> void:
\t_host = host
''' + methods

    sources = {
        "operation_result.gd": '''extends RefCounted

## Final success means that the complete World change is durable.
var ok: bool
var code: String
var message: String
func _init(result: Dictionary) -> void:
\tok = result.get("ok", false)
\tcode = result.get("code", "")
\tmessage = result.get("message", "")
''',
        "data_result.gd": f'''extends "{root}operation_result.gd"

## Only the owning Package interprets this value. This is not a host object.
var value: Variant
func _init(result: Dictionary) -> void:
\tsuper(result)
\tvalue = result.get("value")
''',
        "world_context.gd": f'''extends "{root}operation_result.gd"

var is_authority: bool = false
var is_gm: bool = false
var participant_id: String = ""
func _init(result: Dictionary) -> void:
\tsuper(result)
\tif ok:
\t\tis_authority = result.value.is_authority
\t\tis_gm = result.value.is_gm
\t\tparticipant_id = result.value.participant_id
''',
        "world_data.gd": capability("WorldData", '''
## The authority's one live value for this Package. Null means never committed.
func read() -> DataResult:
\treturn DataResult.new(_host.ReadWorldData())
## Root replacement commits implicitly; invalid input leaves the prior save intact.
func replace(value: Variant) -> OperationResult:
\treturn OperationResult.new(_host.ReplaceWorldData(value))
## Explicitly commit mutations made in place to the live value.
func commit() -> OperationResult:
\treturn OperationResult.new(_host.CommitWorldData())
''', ("OperationResult", "DataResult")),
        "content_reference.gd": '''extends Resource

## Stable Package/local identity. Never a build path or a Package version.
@export var package_id: String
@export var local_id: String
func _init(package: String = "", item: String = "") -> void:
\tpackage_id = package
\tlocal_id = item
''',
        "actor_definition.gd": '''extends Resource

## Override to calculate independent Actor data from a human's submitted choices.
## Rookframe executes this declared Content and owns identity, access and persistence.
func create_data(choices: Variant) -> Variant:
\treturn choices
''',
        "unavailable_capability.gd": capability("UnavailableCapability", '''
var _capability: String
func configure(name: String) -> void:
\t_capability = name
## Integration boundary reserved for the owning project; no predicted gameplay result.
func status() -> OperationResult:
\treturn OperationResult.new(_host.CapabilityStatus(_capability))
''', ("OperationResult",)),
    }
    for name in ("ActorId", "SystemRecordId", "RookId", "SceneId"):
        sources[path(name)] = '''extends RefCounted

var value: String
func _init(identity: String) -> void:
\tvalue = identity
'''
    entity_fields = {
        "Actor": (("ActorId",), [('id', 'ActorId', 'ActorId.new(value.id)'), ('data', 'Variant', 'value.data')]),
        "SystemRecord": (("SystemRecordId",), [('id', 'SystemRecordId', 'SystemRecordId.new(value.id)'), ('type_name', 'String', 'value.type_name'), ('data', 'Variant', 'value.data')]),
        "Rook": (("RookId", "ActorId", "SceneId", "ContentReference"), [('id', 'RookId', 'RookId.new(value.id)'), ('actor', 'ActorId', 'ActorId.new(value.actor) if value.actor != "" else null'), ('scene', 'SceneId', 'SceneId.new(value.scene)'), ('position', 'Vector2', 'value.position'), ('yaw', 'float', 'value.yaw'), ('miniature', 'ContentReference', 'ContentReference.new(raw_miniature.packageId, raw_miniature.localId)')]),
        "Scene": (("SceneId",), [('id', 'SceneId', 'SceneId.new(value.id)'), ('name', 'String', 'value.name')]),
        "ContentEntry": (("ContentReference", "ContentKind"), [('reference', 'ContentReference', 'ContentReference.new(value.packageId, value.localId)'), ('title', 'String', 'value.displayName'), ('kind', 'ContentKind.Value', 'ContentKind.Value.UNKNOWN'), ('available', 'bool', 'value.available')]),
    }
    for name, (types, fields) in entity_fields.items():
        sources[path(name)] = "extends RefCounted\n\n" + imports(*types) + "\n".join(f"var {field}: {type_name}" for field, type_name, _ in fields) + "\nfunc _init(value: Dictionary) -> void:\n" + "\n".join(f"\t{field} = {expression}" for field, _, expression in fields) + "\n"
        if name == "Rook":
            sources[path(name)] = sources[path(name)].replace("func _init(value: Dictionary) -> void:\n", "func _init(value: Dictionary) -> void:\n\tvar raw_miniature: Dictionary = value.miniature\n")
        if name == "ContentEntry":
            for kind in ("actor_definition", "miniature", "prop", "surface_finish", "wall_style"):
                sources[path(name)] += f'\tif value.type == "{kind}":\n\t\tkind = ContentKind.Value.{kind.upper()}\n'
        member = path(name)[:-3]
        for plural in ((False,) if name == "Scene" else (False, True)):
            result_name = name + ("ListResult" if plural else "Result")
            field = "items" if plural else member
            sources[path(result_name)] = f'extends "{root}operation_result.gd"\n\n' + imports(name) + f'var {field}: ' + (f'Array[{name}] = []' if plural else name) + '\nfunc _init(result: Dictionary) -> void:\n\tsuper(result)\n\tif ok:\n' + (f'\t\tvar raw_values: Array = result.value\n\t\tfor value in raw_values:\n\t\t\titems.append({name}.new(value))\n' if plural else f'\t\tvar raw_value: Dictionary = result.value\n\t\t{field} = {name}.new(raw_value)\n')
    sources["actors.gd"] = capability("Actors", '''
func list() -> ActorListResult:
\treturn ActorListResult.new(_host.ListActors())
func read(id: ActorId) -> ActorResult:
\treturn ActorResult.new(_host.ReadActor(id.value))
func create(definition: ContentReference, choices: Variant) -> ActorResult:
\treturn ActorResult.new(_host.CreateActor(definition.package_id, definition.local_id, choices))
func update(id: ActorId, data: Variant) -> ActorResult:
\treturn ActorResult.new(_host.UpdateActor(id.value, data))
func delete(id: ActorId) -> OperationResult:
\treturn OperationResult.new(_host.DeleteActor(id.value))
''', ("ActorId", "ActorResult", "ActorListResult", "ContentReference", "OperationResult"))
    sources["system_records.gd"] = capability("SystemRecords", '''
func list(type_name: String = "") -> SystemRecordListResult:
\treturn SystemRecordListResult.new(_host.ListSystemRecords(type_name))
func read(id: SystemRecordId) -> SystemRecordResult:
\treturn SystemRecordResult.new(_host.ReadSystemRecord(id.value))
func create(type_name: String, data: Variant) -> SystemRecordResult:
\treturn SystemRecordResult.new(_host.CreateSystemRecord(type_name, data))
func update(id: SystemRecordId, data: Variant) -> SystemRecordResult:
\treturn SystemRecordResult.new(_host.UpdateSystemRecord(id.value, data))
func delete(id: SystemRecordId) -> OperationResult:
\treturn OperationResult.new(_host.DeleteSystemRecord(id.value))
''', ("SystemRecordId", "SystemRecordResult", "SystemRecordListResult", "OperationResult"))
    sources["rooks.gd"] = capability("Rooks", '''
func list() -> RookListResult:
\treturn RookListResult.new(_host.ListRooks())
func read(id: RookId) -> RookResult:
\treturn RookResult.new(_host.ReadRook(id.value))
func create(miniature: ContentReference, scene: SceneId, position: Vector2, yaw: float = 0.0) -> RookResult:
\treturn RookResult.new(_host.CreateRook(miniature.package_id, miniature.local_id, scene.value, position, yaw))
func move(id: RookId, position: Vector2, yaw: float = 0.0) -> RookResult:
\treturn RookResult.new(_host.MoveRook(id.value, position, yaw))
func link(id: RookId, actor: ActorId) -> OperationResult:
\treturn OperationResult.new(_host.LinkRook(id.value, actor.value))
func unlink(id: RookId) -> OperationResult:
\treturn OperationResult.new(_host.UnlinkRook(id.value))
func delete(id: RookId) -> OperationResult:
\treturn OperationResult.new(_host.DeleteRook(id.value))
''', ("RookId", "ActorId", "RookResult", "RookListResult", "SceneId", "ContentReference", "OperationResult"))
    sources["distance_result.gd"] = f'''extends "{root}operation_result.gd"

## Logical center-to-center distance in the current Scene's tabletop units.
var distance: float
func _init(result: Dictionary) -> void:
\tsuper(result)
\tif ok:
\t\tdistance = result.value
'''
    sources["scenes.gd"] = capability("Scenes", '''
func current() -> SceneResult:
\treturn SceneResult.new(_host.CurrentScene())
func distance(from: RookId, to: RookId) -> DistanceResult:
\treturn DistanceResult.new(_host.RookDistance(from.value, to.value))
''', ("RookId", "SceneResult", "DistanceResult"))
    sources["content.gd"] = capability("Content", '''
func list(kind: ContentKind.Value = ContentKind.Value.ALL) -> ContentEntryListResult:
\treturn ContentEntryListResult.new(_host.ListContent(kind))
func read(reference: ContentReference) -> ContentEntryResult:
\treturn ContentEntryResult.new(_host.ReadContent(reference.package_id, reference.local_id))
''', ("ContentReference", "ContentEntryResult", "ContentEntryListResult", "ContentKind"))
    sources["content_kind.gd"] = '''extends RefCounted

enum Value { UNKNOWN = -1, ALL, ACTOR_DEFINITION, MINIATURE, PROP, SURFACE_FINISH, WALL_STYLE }
'''
    sources["windows.gd"] = capability("Windows", '''
func open(surface: ExtensionSurface) -> void:
\t_host.OpenWindow(surface.scene)
''', ("ExtensionSurface",))
    return sources
