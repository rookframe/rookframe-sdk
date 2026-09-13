"""Typed checked integrations. Only the generated implementation sees transport dictionaries."""
import re


def service_sources(root: str) -> dict[str, str]:
    def path(name):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower() + ".gd"

    def imports(*names):
        return "".join(f'const {name} = preload("{root}{path(name)}")\n' for name in names)

    def start_request(anonymous: str, authenticated: str, arguments: str) -> str:
        # Keep the native account binding and scope check in one generator seam.
        return f'''\tvar started: Dictionary
\tif _account == null:
\t\tstarted = _scope._host.{anonymous}({arguments})
\telif _account._scope != _scope:
\t\tstarted = {{"ok": false, "code": "scope_mismatch", "message": "Use an account from this SDK scope."}}
\telse:
\t\tstarted = _scope._host.{authenticated}(_account._provider, _account._area, _account._entry, {arguments}, _account.refresh_policy)
'''

    sources = {
        "integration_result.gd": f'''extends "{root}operation_result.gd"
## A completed outcome; pending state belongs to Rookframe.
var retry_after: int
func _init(result: Dictionary) -> void:
\tsuper(result)
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
        "response_result.gd": f'''extends "{root}bytes_result.gd"
## Transport success is separate from the provider's HTTP status.
var status: int
var text: String
func _init(result: Dictionary) -> void:
\tsuper(result)
\tstatus = result.get("status", 0)
\ttext = result.get("text", "")
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
        "network.gd": 'extends RefCounted\n' + imports("ServiceDefinition", "NamedService", "Account") + '''
var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
\t_scope = scope
func service(definition: ServiceDefinition, account: Account = null) -> NamedService:
\treturn NamedService.new(_scope, definition.name, account)
''',
        "named_service.gd": 'extends RefCounted\n' + imports("HttpMethod", "RequestHeaders", "ResponseResult", "Account") + '''
var _scope: ServiceScope
var _name: String
var _account: Account
func _init(scope: ServiceScope, name: String, account: Account = null) -> void:
\t_scope = scope
\t_name = name
\t_account = account
func request(path: String, method: HttpMethod.Value = HttpMethod.Value.GET, body: String = "", headers: RequestHeaders = null) -> ResponseResult:
\tvar provider_headers: RequestHeaders = headers if headers != null else RequestHeaders.new()
''' + start_request('RequestServiceWithHeaders', 'RequestAccountService', '_name, path, HttpMethod.new()._text(method), body, provider_headers._copy()') + '''
\treturn ResponseResult.new(await _scope._complete(started))
''',
    })
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
    for kind, selected, result in (
        ("file", "ScopedFile", "FileSelectionResult"),
        ("folder", "ScopedFolder", "FolderSelectionResult"),
    ):
        sources[path(result)] = f'extends "{root}integration_result.gd"\n' + imports(selected) + f'''
var {kind}: {selected}
func _init(result: Dictionary, selection: {selected}) -> void:
\tsuper(result)
\t{kind} = selection
'''
        sources["file_area.gd"] += imports(result) + f'''
func select_{kind}() -> {result}:
\tvar result: Dictionary = await _scope._complete(_scope._host.SelectFile(_area, {str(kind == 'folder').lower()}))
\tvar selected: {selected}
\tif result.get("ok", false):
\t\tselected = {selected}.new(_scope, _area, result.get("text", ""))
\treturn {result}.new(result, selected)
'''
    sources["scoped_stream.gd"] = 'extends RefCounted\n' + imports("BytesResult", "IntegrationResult") + '''
var _scope: ServiceScope
var _id: int
func _init(scope: ServiceScope, id: int) -> void:
\t_scope = scope
\t_id = id
func read(maximum_bytes: int = 65536) -> BytesResult:
\treturn BytesResult.new(await _scope._complete(_scope._host.ReadServiceStream(_id, maximum_bytes)))
func close() -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.CloseServiceStream(_id))
'''
    sources["stream_result.gd"] = f'extends "{root}integration_result.gd"\n' + imports("ScopedStream") + '''
var stream: ScopedStream
func _init(result: Dictionary, opened: ScopedStream) -> void:
\tsuper(result)
\tstream = opened
'''
    sources["named_service.gd"] += imports("StreamResult", "ScopedStream", "ScopedFile", "IntegrationResult") + '''
func open_stream(path: String) -> StreamResult:
''' + start_request('OpenServiceStream', 'OpenAccountStream', '_name, path') + '''
\tvar result: Dictionary = await _scope._complete(started)
\tvar stream: ScopedStream
\tif result.get("ok", false):
\t\tstream = ScopedStream.new(_scope, result.get("id", 0))
\treturn StreamResult.new(result, stream)
func download(path: String, target: ScopedFile) -> IntegrationResult:
\tif target._scope != _scope:
\t\treturn IntegrationResult.new({"ok": false, "code": "scope_mismatch", "message": "Use a file from this SDK scope."})
''' + start_request('DownloadFile', 'DownloadAccountFile', '_name, path, target._area, target._path') + '''
\treturn IntegrationResult.new(await _scope._complete(started))
func upload(path: String, source: ScopedFile, method: HttpMethod.Value = HttpMethod.Value.POST) -> ResponseResult:
\tif source._scope != _scope:
\t\treturn ResponseResult.new({"ok": false, "code": "scope_mismatch", "message": "Use a file from this SDK scope."})
''' + start_request('UploadFile', 'UploadAccountFile', '_name, path, HttpMethod.new()._text(method), source._area, source._path') + '''
\treturn ResponseResult.new(await _scope._complete(started))
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
## Native signal ownership handles main-thread delivery and discards continuations at stop.
func _complete(started: Dictionary, authentication: bool = false) -> Dictionary:
\tif started.get("ready", true):
\t\treturn started
\treturn await _host.ServiceCompletion(started.get("id", 0), authentication)
'''
    for name, source in sources.items():
        if "scope: ServiceScope" in source:
            first, rest = source.split("\n", 1)
            sources[name] = first + "\n" + imports("ServiceScope") + rest
    return sources
