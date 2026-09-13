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
        "authentication.gd": 'extends RefCounted\n' + imports("SecretSetting", "SettingsScope", "Account") + '''
var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
\t_scope = scope
## Bind the configured provider and protected destination once.
func account(setting: SecretSetting, area: SettingsScope.Kind = SettingsScope.Kind.USER) -> Account:
\tvar provider: String = setting.authentication.name if setting.authentication != null else ""
\treturn Account.new(_scope, provider, "world" if area == SettingsScope.Kind.WORLD else "user", setting.key)
''',
        "account_status.gd": f'''extends "{root}integration_result.gd"
enum State {{ UNAVAILABLE, SIGNED_OUT, SIGNED_IN, EXPIRED }}
var state: State
func _init(result: Dictionary) -> void:
\tsuper(result)
\tstate = result.get("state", State.UNAVAILABLE)
''',
        "account.gd": 'extends RefCounted\n' + imports("IntegrationResult", "ProviderTokenResult", "AccountStatus") + '''
enum RefreshPolicy { EXPLICIT, WHEN_EXPIRED }
## Preflight refresh only. HTTP failures never replay a request or launch sign-in.
var refresh_policy: RefreshPolicy = RefreshPolicy.WHEN_EXPIRED
var _scope: ServiceScope
var _provider: String
var _area: String
var _entry: String
func _init(scope: ServiceScope, provider: String, area: String, entry: String) -> void:
\t_scope = scope
\t_provider = provider
\t_area = area
\t_entry = entry
func status() -> AccountStatus:
\treturn AccountStatus.new(_scope._host.AccountStatus(_provider, _area, _entry))
func read_tokens() -> ProviderTokenResult:
\treturn ProviderTokenResult.new(_scope._host.ReadAccountTokens(_provider, _area, _entry))
func sign_in() -> IntegrationResult:
\treturn IntegrationResult.new(await _scope._complete(_scope._host.StartAuthentication(_provider, _area, _entry), true))
func refresh() -> IntegrationResult:
\treturn IntegrationResult.new(await _scope._complete(_scope._host.RefreshSecret(_provider, _area, _entry)))
func clear() -> IntegrationResult:
\treturn IntegrationResult.new(_scope._host.RevokeSecret(_area, _entry))
''',
        "browser.gd": 'extends RefCounted\n' + imports("IntegrationResult") + '''
var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
\t_scope = scope
func open(url: String) -> IntegrationResult:
\treturn IntegrationResult.new(await _scope._complete(_scope._host.OpenBrowserLink(url)))
''',
    }
    return sources
