extends "res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/sdk/implementation.gd"
const API_KEY: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/api_key.tres")
const ACCOUNT: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/account.tres")
const WORLD_KEY: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/world_key.tres")
const WORLD_ACCOUNT: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/world_account.tres")
func describe_settings() -> SDK.SettingsRegistration:
	var registration: SDK.SettingsRegistration = SDK.SettingsRegistration.new()
	registration.user = [API_KEY, ACCOUNT]
	registration.world = [WORLD_KEY, WORLD_ACCOUNT]
	return registration
