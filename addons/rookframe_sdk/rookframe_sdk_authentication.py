"""Protected entries and deliberate browser authentication over the shared service scope."""


def authentication_sources(root, imports):
    sources = {
        "authentication_provider_definition.gd": '''extends Resource
## Matches an admitted authentication.json provider. Contains no confidential credential.
@export var name: String
''',
        "secret_result.gd": f'''extends "{root}text_result.gd"
var found: bool
func _init(result: Dictionary) -> void:
\tsuper(result)
\tfound = result.get("found", false)
''',
        "provider_tokens.gd": '''extends RefCounted
## Raw credentials are authorized for this owning Package's checked API requests.
var access_token: String
var token_type: String
var refresh_token: String
var scope: String
var has_expiry: bool
var expires_at: int
func _init(result: Dictionary) -> void:
\taccess_token = result.get("access_token", "")
\ttoken_type = result.get("token_type", "")
\trefresh_token = result.get("refresh_token", "")
\tscope = result.get("scope", "")
\thas_expiry = result.get("has_expiry", false)
\texpires_at = result.get("expires_at", 0)
''',
        "provider_token_result.gd": f'extends "{root}integration_result.gd"\n' + imports("ProviderTokens") + '''
var found: bool
var tokens: ProviderTokens
func _init(result: Dictionary) -> void:
\tsuper(result)
\tfound = result.get("found", false)
\tif ok and found:
\t\ttokens = ProviderTokens.new(result)
''',
        "secrets.gd": 'extends RefCounted\n' + imports("SecretArea") + '''
var _user: SecretArea
var _world: SecretArea
var user: SecretArea:
\tget:
\t\treturn _user
var world: SecretArea:
\tget:
\t\treturn _world
func _init(scope: ServiceScope) -> void:
\t_user = SecretArea.new(scope, "user")
\t_world = SecretArea.new(scope, "world")
''',
        "secret_area.gd": 'extends RefCounted\n' + imports("SecretEntry", "SecretSetting") + '''
var _scope: ServiceScope
var _area: String
func _init(scope: ServiceScope, area: String) -> void:
\t_scope = scope
\t_area = area
func entry(name: String) -> SecretEntry:
\treturn SecretEntry.new(_scope, _area, name)
func setting(descriptor: SecretSetting) -> SecretEntry:
\treturn entry(descriptor.key)
''',
        "secret_entry.gd": 'extends RefCounted\n' + imports("SecretResult", "ProviderTokenResult", "IntegrationResult") + '''
var _scope: ServiceScope
var _area: String
var _entry: String
func _init(scope: ServiceScope, area: String, name: String) -> void:
\t_scope = scope
\t_area = area
\t_entry = name
func read() -> SecretResult:
\treturn SecretResult.new(_scope._host.ReadSecret(_area, _entry))
func read_tokens() -> ProviderTokenResult:
\treturn ProviderTokenResult.new(_scope._host.ReadProviderTokens(_area, _entry))
func write(value: String) -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.WriteSecret(_area, _entry, value))
func clear() -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.RevokeSecret(_area, _entry))
''',
        "authentication.gd": 'extends RefCounted\n' + imports("AuthenticationProviderDefinition", "AuthenticationProvider") + '''
var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
\t_scope = scope
func provider(definition: AuthenticationProviderDefinition) -> AuthenticationProvider:
\treturn AuthenticationProvider.new(_scope, definition.name)
''',
        "authentication_provider.gd": 'extends RefCounted\n' + imports("SecretEntry", "AuthenticationOperation", "IntegrationOperation") + '''
var _scope: ServiceScope
var _name: String
func _init(scope: ServiceScope, name: String) -> void:
\t_scope = scope
\t_name = name
## Rookframe confirms Package, destination and purpose before opening any browser.
func sign_in(destination: SecretEntry) -> AuthenticationOperation:
\tif destination._scope != _scope:
\t\treturn AuthenticationOperation.new(_scope, {"ok": false, "code": "scope_mismatch", "message": "Use a secret from this SDK scope."})
\treturn AuthenticationOperation.new(_scope, _scope._host.StartAuthentication(_name, destination._area, destination._entry))
func refresh(destination: SecretEntry) -> IntegrationOperation:
\tif destination._scope != _scope:
\t\treturn IntegrationOperation.new(_scope, {"ok": false, "code": "scope_mismatch", "message": "Use a secret from this SDK scope."})
\treturn IntegrationOperation.new(_scope, _scope._host.RefreshSecret(_name, destination._area, destination._entry))
''',
        "authentication_result.gd": f'''extends "{root}integration_result.gd"
enum Phase {{ CONFIRMATION, BROWSER, COMPLETED, FAILED }}
var phase: Phase
func _init(result: Dictionary) -> void:
\tsuper(result)
\tphase = Phase.CONFIRMATION
\tif not ok:
\t\tphase = Phase.FAILED
\telif result.get("state", "") == "completed":
\t\tphase = Phase.COMPLETED
\telif result.get("state", "") == "pending":
\t\tphase = Phase.BROWSER
''',
        "authentication_operation.gd": 'extends RefCounted\n' + imports("PendingOperation", "AuthenticationResult") + '''
var _scope: ServiceScope
var _launch: PendingOperation
var _final: AuthenticationResult
func _init(scope: ServiceScope, started: Dictionary) -> void:
\t_scope = scope
\t_launch = PendingOperation.new(scope, started)
func poll() -> AuthenticationResult:
\tif _final != null:
\t\treturn _final
\tvar result: Dictionary = _launch._consume()
\tif result.get("ready", true) and result.get("ok", false):
\t\tvar transaction: String = result.get("text", "")
\t\tresult = _scope._host.PollAuthentication(transaction)
\tvar status: AuthenticationResult = AuthenticationResult.new(result)
\tif status.ready:
\t\t_final = status
\treturn status
''',
        "browser.gd": 'extends RefCounted\n' + imports("IntegrationOperation") + '''
var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
\t_scope = scope
func open(url: String) -> IntegrationOperation:
\treturn IntegrationOperation.new(_scope, _scope._host.OpenBrowserLink(url))
''',
    }
    return sources
