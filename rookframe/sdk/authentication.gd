extends RefCounted
const ServiceScope = preload("res://rookframe/sdk/service_scope.gd")
const SecretSetting = preload("res://rookframe/sdk/secret_setting.gd")
const SettingsScope = preload("res://rookframe/sdk/settings_scope.gd")
const Account = preload("res://rookframe/sdk/account.gd")

var _scope: ServiceScope
func _init(scope: ServiceScope) -> void:
	_scope = scope
## Bind the configured provider and protected destination once.
func account(setting: SecretSetting, area: SettingsScope.Kind = SettingsScope.Kind.USER) -> Account:
	var provider: String = setting.authentication.name if setting.authentication != null else ""
	return Account.new(_scope, provider, "world" if area == SettingsScope.Kind.WORLD else "user", setting.key)
