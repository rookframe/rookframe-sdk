extends "res://rookframe/sdk/setting.gd"
## Values use the existing protected store and never enter an ordinary draft/copy.

const AuthenticationProviderDefinition = preload("res://rookframe/sdk/authentication_provider_definition.gd")
## Optional provider for Rookframe-owned sign-in/refresh/clear controls.
@export var authentication: AuthenticationProviderDefinition
