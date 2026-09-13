"""Typed checked integrations. Only the generated implementation sees transport dictionaries."""
import re


def service_sources(root: str) -> dict[str, str]:
    def path(name):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + ".gd"

    def imports(*names):
        return "".join(f'const {name} = preload("{root}{path(name)}")\n' for name in names)

    sources = {
        "integration_result.gd": f'''extends "{root}operation_result.gd"
## ready=false means pending, not successful completion. No native handle escapes.
var ready: bool
var retry_after: int
func _init(result: Dictionary) -> void:
\tsuper(result)
\tready = result.get("ready", true)
\tretry_after = result.get("retry_after", 0)
''',
        "text_result.gd": f'''extends "{root}integration_result.gd"
var text: String
func _init(result: Dictionary) -> void:
\tsuper(result)
\ttext = result.get("text", "")
''',
        "bytes_result.gd": f'''extends "{root}integration_result.gd"
var data: PackedByteArray = []
func _init(result: Dictionary) -> void:
\tsuper(result)
\tdata = result.get("data", [])
''',
        "clipboard.gd": 'extends RefCounted\n' + imports("IntegrationResult", "TextResult") + '''
var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
\t_scope = scope
func read_text() -> TextResult:
\treturn TextResult.new(_scope._host.ReadClipboard())
func write_text(text: String) -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.WriteClipboard(text))
''',
        "files.gd": 'extends RefCounted\n' + imports("FileArea") + '''
var _package: FileArea
var _user: FileArea
var _world: FileArea
var package: FileArea:
\tget:
\t\treturn _package
var user: FileArea:
\tget:
\t\treturn _user
var world: FileArea:
\tget:
\t\treturn _world
func _init(scope: ServiceScope) -> void:
\t_package = FileArea.new(scope, "package")
\t_user = FileArea.new(scope, "user")
\t_world = FileArea.new(scope, "world")
''',
        "file_area.gd": 'extends RefCounted\n' + imports("ScopedFile", "ScopedFolder") + '''
var _scope: ServiceScope
var _area: String
func _init(scope: ServiceScope, area: String) -> void:
\t_scope = scope
\t_area = area
## Relative names are validated by the host on each use. A value grants no new authority.
func file(relative_name: String) -> ScopedFile:
\treturn ScopedFile.new(_scope, _area, relative_name)
func folder(relative_name: String) -> ScopedFolder:
\treturn ScopedFolder.new(_scope, _area, relative_name)
''',
        "scoped_file.gd": 'extends RefCounted\n' + imports("TextResult", "BytesResult", "IntegrationResult") + '''
var _scope: ServiceScope
var _area: String
var _path: String
func _init(scope: ServiceScope, area: String, relative_name: String) -> void:
\t_scope = scope
\t_area = area
\t_path = relative_name
func read_text() -> TextResult:
\treturn TextResult.new(_scope._host.ReadText(_area, _path))
func read_bytes() -> BytesResult:
\treturn BytesResult.new(_scope._host.ReadFile(_area, _path))
## Immutable Package content always refuses writes.
func write_text(text: String) -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.WriteText(_area, _path, text))
func write_bytes(data: PackedByteArray) -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.WriteFile(_area, _path, data))
''',
        "scoped_folder.gd": 'extends RefCounted\n' + imports("ScopedFile") + '''
var _scope: ServiceScope
var _area: String
var _path: String
func _init(scope: ServiceScope, area: String, relative_name: String) -> void:
\t_scope = scope
\t_area = area
\t_path = relative_name
func file(relative_name: String) -> ScopedFile:
\treturn ScopedFile.new(_scope, _area, (_path + "/" if not _path.is_empty() else "") + relative_name)
''',
    }
    sources.update({
        "pending_operation.gd": '''extends RefCounted
## Internal polling bridge. Completed results are retained; native IDs are consumed once.
var _scope: ServiceScope
var _last: Dictionary
var _id: int
func _init(scope: ServiceScope, started: Dictionary) -> void:
\t_scope = scope
\t_last = started
\t_id = started.get("id", 0)
func _consume() -> Dictionary:
\tif not _last.get("ready", true):
\t\t_last = _scope._host.PollService(_id)
\treturn _last
''',
        "response_result.gd": f'''extends "{root}bytes_result.gd"
## Transport success is separate from the provider's HTTP status.
var status: int
var text: String
func _init(result: Dictionary) -> void:
\tsuper(result)
\tstatus = result.get("status", 0)
\ttext = result.get("text", "")
''',
        "request_operation.gd": 'extends RefCounted\n' + imports("PendingOperation", "ResponseResult") + '''
var _pending: PendingOperation
func _init(scope: ServiceScope, started: Dictionary) -> void:
\t_pending = PendingOperation.new(scope, started)
func poll() -> ResponseResult:
\treturn ResponseResult.new(_pending._consume())
''',
        "service_definition.gd": '''extends Resource
## Matches one admitted services.json declaration; never grants private access.
@export var name: String
''',
        "http_method.gd": '''extends RefCounted
enum Value { GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS }
func _text(value: Value) -> String:
\tif value == Value.GET:
\t\treturn "GET"
\tif value == Value.POST:
\t\treturn "POST"
\tif value == Value.PUT:
\t\treturn "PUT"
\tif value == Value.PATCH:
\t\treturn "PATCH"
\tif value == Value.DELETE:
\t\treturn "DELETE"
\tif value == Value.HEAD:
\t\treturn "HEAD"
\tif value == Value.OPTIONS:
\t\treturn "OPTIONS"
\treturn ""
''',
        "request_headers.gd": '''extends RefCounted
## Only these provider headers cross the checked destination boundary.
var authorization: String = ""
var accept: String = ""
var content_type: String = ""
var if_match: String = ""
var if_none_match: String = ""
var api_key: String = ""
func _copy() -> Dictionary:
\tvar headers: Dictionary = {}
\tif not authorization.is_empty():
\t\theaders["Authorization"] = authorization
\tif not accept.is_empty():
\t\theaders["Accept"] = accept
\tif not content_type.is_empty():
\t\theaders["Content-Type"] = content_type
\tif not if_match.is_empty():
\t\theaders["If-Match"] = if_match
\tif not if_none_match.is_empty():
\t\theaders["If-None-Match"] = if_none_match
\tif not api_key.is_empty():
\t\theaders["X-Api-Key"] = api_key
\treturn headers
''',
        "network.gd": 'extends RefCounted\n' + imports("ServiceDefinition", "NamedService") + '''
var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
\t_scope = scope
func service(definition: ServiceDefinition) -> NamedService:
\treturn NamedService.new(_scope, definition.name)
''',
        "named_service.gd": 'extends RefCounted\n' + imports("HttpMethod", "RequestHeaders", "RequestOperation") + '''
var _scope: ServiceScope
var _name: String
func _init(scope: ServiceScope, name: String) -> void:
\t_scope = scope
\t_name = name
func request(path: String, method: HttpMethod.Value = HttpMethod.Value.GET, body: String = "", headers: RequestHeaders = null) -> RequestOperation:
\tvar provider_headers: RequestHeaders = headers if headers != null else RequestHeaders.new()
\treturn RequestOperation.new(_scope, _scope._host.RequestServiceWithHeaders(_name, path, HttpMethod.new()._text(method), body, provider_headers._copy()))
''',
    })
    for name, result in (("integration_operation", "IntegrationResult"), ("bytes_operation", "BytesResult")):
        sources[name + ".gd"] = 'extends RefCounted\n' + imports("PendingOperation", result) + f'''
var _pending: PendingOperation
func _init(scope: ServiceScope, started: Dictionary) -> void:
\t_pending = PendingOperation.new(scope, started)
func poll() -> {result}:
\treturn {result}.new(_pending._consume())
'''
    sources["portrait_result.gd"] = f'''extends "{root}integration_result.gd"
## A decoded, fitted 512 x 512 native image. No Script/Resource file is evaluated.
var texture: Texture2D
func _init(result: Dictionary) -> void:
\tsuper(result)
\ttexture = result.get("texture", null)
'''
    sources["scoped_file.gd"] += imports("PortraitResult") + '''
func read_portrait() -> PortraitResult:
\treturn PortraitResult.new(_scope._host.DecodePortrait(_area, _path))
'''
    for kind, selected, result, operation in (
        ("file", "ScopedFile", "FileSelectionResult", "FileSelection"),
        ("folder", "ScopedFolder", "FolderSelectionResult", "FolderSelection"),
    ):
        sources[path(result)] = f'extends "{root}integration_result.gd"\n' + imports(selected) + f'''
var {kind}: {selected}
func _init(result: Dictionary, selection: {selected}) -> void:
\tsuper(result)
\t{kind} = selection
'''
        sources[path(operation)] = 'extends RefCounted\n' + imports("PendingOperation", selected, result) + f'''
var _pending: PendingOperation
var _scope: ServiceScope
var _area: String
var _selection: {selected}
func _init(scope: ServiceScope, area: String, started: Dictionary) -> void:
\t_scope = scope
\t_area = area
\t_pending = PendingOperation.new(scope, started)
func poll() -> {result}:
\tvar result: Dictionary = _pending._consume()
\tif _selection == null and result.get("ready", true) and result.get("ok", false):
\t\t_selection = {selected}.new(_scope, _area, result.get("text", ""))
\treturn {result}.new(result, _selection)
'''
        sources["file_area.gd"] += imports(operation) + f'''
func select_{kind}() -> {operation}:
\treturn {operation}.new(_scope, _area, _scope._host.SelectFile(_area, {str(kind == 'folder').lower()}))
'''
    sources["scoped_stream.gd"] = 'extends RefCounted\n' + imports("BytesOperation", "IntegrationResult") + '''
var _scope: ServiceScope
var _id: int
func _init(scope: ServiceScope, id: int) -> void:
\t_scope = scope
\t_id = id
func read(maximum_bytes: int = 65536) -> BytesOperation:
\treturn BytesOperation.new(_scope, _scope._host.ReadServiceStream(_id, maximum_bytes))
func close() -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.CloseServiceStream(_id))
'''
    sources["stream_result.gd"] = f'extends "{root}integration_result.gd"\n' + imports("ScopedStream") + '''
var stream: ScopedStream
func _init(result: Dictionary, opened: ScopedStream) -> void:
\tsuper(result)
\tstream = opened
'''
    sources["stream_operation.gd"] = 'extends RefCounted\n' + imports("PendingOperation", "StreamResult", "ScopedStream") + '''
var _scope: ServiceScope
var _pending: PendingOperation
var _stream: ScopedStream
func _init(scope: ServiceScope, started: Dictionary) -> void:
\t_scope = scope
\t_pending = PendingOperation.new(scope, started)
func poll() -> StreamResult:
\tvar result: Dictionary = _pending._consume()
\tif _stream == null and result.get("ready", true) and result.get("ok", false):
\t\t_stream = ScopedStream.new(_scope, result.get("id", 0))
\treturn StreamResult.new(result, _stream)
'''
    sources["named_service.gd"] += imports("StreamOperation", "ScopedFile", "IntegrationOperation") + '''
func open_stream(path: String) -> StreamOperation:
\treturn StreamOperation.new(_scope, _scope._host.OpenServiceStream(_name, path))
func download(path: String, target: ScopedFile) -> IntegrationOperation:
\tif target._scope != _scope:
\t\treturn IntegrationOperation.new(_scope, {"ok": false, "code": "scope_mismatch", "message": "Use a file from this SDK scope."})
\treturn IntegrationOperation.new(_scope, _scope._host.DownloadFile(_name, path, target._area, target._path))
func upload(path: String, source: ScopedFile, method: HttpMethod.Value = HttpMethod.Value.POST) -> RequestOperation:
\tif source._scope != _scope:
\t\treturn RequestOperation.new(_scope, {"ok": false, "code": "scope_mismatch", "message": "Use a file from this SDK scope."})
\treturn RequestOperation.new(_scope, _scope._host.UploadFile(_name, path, HttpMethod.new()._text(method), source._area, source._path))
'''
    sources["file_location.gd"] = '''extends RefCounted
enum Area { PACKAGE, USER, WORLD }
func _text(area: Area) -> String:
\tif area == Area.PACKAGE:
\t\treturn "package"
\tif area == Area.USER:
\t\treturn "user"
\tif area == Area.WORLD:
\t\treturn "world"
\treturn ""
func _value(area: String) -> Area:
\tif area == "package":
\t\treturn Area.PACKAGE
\tif area == "world":
\t\treturn Area.WORLD
\treturn Area.USER
'''
    for kind, reference, scoped in (("file", "InternalFileReference", "ScopedFile"),
                                    ("folder", "InternalFolderReference", "ScopedFolder")):
        sources[path(reference)] = 'extends Resource\n' + imports("FileLocation") + '''
## Portable relative identity in this Package's current areas, never an OS path or grant.
@export var area: FileLocation.Area = FileLocation.Area.USER
@export var name: String
func _init(location: FileLocation.Area = FileLocation.Area.USER, relative_name: String = "") -> void:
\tarea = location
\tname = relative_name
'''
        sources[f"scoped_{kind}.gd"] += imports("FileLocation", reference) + f'''
## Retain this value in Package-owned data to reopen through a fresh authorized SDK.
func to_reference() -> {reference}:
\treturn {reference}.new(FileLocation.new()._value(_area), _path)
'''
        sources["files.gd"] += imports(reference, scoped) + f'''
func {"open" if kind == "file" else "open_folder"}(reference: {reference}) -> {scoped}:
\treturn {scoped}.new(_scope, FileLocation.new()._text(reference.area), reference.name)
'''
    sources["files.gd"] = sources["files.gd"].replace("var _package: FileArea", imports("FileLocation") + "var _scope: ServiceScope\nvar _package: FileArea")
    sources["files.gd"] = sources["files.gd"].replace("\t_package =", "\t_scope = scope\n\t_package =", 1)
    from rookframe_sdk_authentication import authentication_sources
    sources.update(authentication_sources(root, imports))
    sources["service_scope.gd"] = '''extends RefCounted
## Internal Package binding shared by every typed integration value.
var _host: Object
func _init(host: Object) -> void:
\t_host = host
'''
    for name, source in sources.items():
        if "scope: ServiceScope" in source:
            first, rest = source.split("\n", 1)
            sources[name] = first + "\n" + imports("ServiceScope") + rest
    return sources
