extends RefCounted

const Rail = preload("res://rookframe/sdk/rail.gd")
const Rails = preload("res://rookframe/sdk/rails.gd")
const WindowButton = preload("res://rookframe/sdk/window_button.gd")
const ExtensionSurface = preload("res://rookframe/sdk/extension_surface.gd")
const SDK_EDITION := "2029"
const MINIMUM_REVISION := 35

var _host: Object
var _rails: Rails
## Package-scoped access to the workspace Rails.
var rails: Rails:
	get:
		return _rails


func _init(host: Object) -> void:
	_host = host
	_service_scope = ServiceScope.new(host)
	_portraits = ActorPortraits.new(_service_scope)
	_browser = Browser.new(_service_scope)
	_authentication = Authentication.new(_service_scope)
	_secrets = Secrets.new(_service_scope)
	_network = Network.new(_service_scope)
	_clipboard = Clipboard.new(_service_scope)
	_files = Files.new(_service_scope)
	_settings = Settings.new(host)
	_host.WorldChanged.connect(_world_changed)
	_announcements = Announcements.new(host)
	_action_log = ActionLog.new(host)
	_system_actions = SystemActions.new(host)
	_dice = Dice.new(host)
	_targeting = Targeting.new(host)
	_builder = UnavailableCapability.new(host)
	_builder.configure("builder")
	_windows = Windows.new(host)
	_content = Content.new(host)
	_scenes = Scenes.new(host)
	_rooks = Rooks.new(host)
	_system_records = SystemRecords.new(host)
	_public_identities = PublicIdentities.new(host)
	_actors = Actors.new(host)
	_world_data = WorldData.new(host)
	_rails = Rails.new(host)
	_character_hud = CharacterHud.new(host)
	_huds = Huds.new(host)
	_ui_root = ContributionSlot.new(host, "ui-root")
	_slots = Slots.new(host)
	_feedback = Feedback.new(host)
	_translations = Translations.new(host)


## Stable Package identity, independent of builds and installations.
func package_id() -> String:
	return _host.PackageId()


## Current admitted resource root for this Package.
func package_root() -> String:
	return _host.PackageRoot()


## Current desktop, tablet or phone Presentation experience.
func presentation_experience() -> DeviceExperience:
	return DeviceExperience.new(_host.PresentationDevice())

const Contribution = preload("res://rookframe/sdk/contribution.gd")
const ContributionSlot = preload("res://rookframe/sdk/contribution_slot.gd")
const Slots = preload("res://rookframe/sdk/slots.gd")
const Feedback = preload("res://rookframe/sdk/feedback.gd")
const FeedbackMessage = preload("res://rookframe/sdk/feedback_message.gd")
const FeedbackAction = preload("res://rookframe/sdk/feedback_action.gd")
const Translations = preload("res://rookframe/sdk/translations.gd")
const Cleanup = preload("res://rookframe/sdk/cleanup.gd")
const DeviceExperience = preload("res://rookframe/sdk/device_experience.gd")

var _ui_root: ContributionSlot
var ui_root: ContributionSlot:
	get:
		return _ui_root

var _slots: Slots
var slots: Slots:
	get:
		return _slots

var _feedback: Feedback
var feedback: Feedback:
	get:
		return _feedback

var _translations: Translations
var translations: Translations:
	get:
		return _translations

const OperationResult = preload("res://rookframe/sdk/operation_result.gd")
const DataResult = preload("res://rookframe/sdk/data_result.gd")
const WorldContext = preload("res://rookframe/sdk/world_context.gd")
const WorldData = preload("res://rookframe/sdk/world_data.gd")
const ContentReference = preload("res://rookframe/sdk/content_reference.gd")
const ActorDefinition = preload("res://rookframe/sdk/actor_definition.gd")
const UnavailableCapability = preload("res://rookframe/sdk/unavailable_capability.gd")
const ActorId = preload("res://rookframe/sdk/actor_id.gd")
const SystemRecordId = preload("res://rookframe/sdk/system_record_id.gd")
const RookId = preload("res://rookframe/sdk/rook_id.gd")
const SceneId = preload("res://rookframe/sdk/scene_id.gd")
const Actor = preload("res://rookframe/sdk/actor.gd")
const ActorResult = preload("res://rookframe/sdk/actor_result.gd")
const ActorListResult = preload("res://rookframe/sdk/actor_list_result.gd")
const SystemRecord = preload("res://rookframe/sdk/system_record.gd")
const SystemRecordResult = preload("res://rookframe/sdk/system_record_result.gd")
const SystemRecordListResult = preload("res://rookframe/sdk/system_record_list_result.gd")
const Rook = preload("res://rookframe/sdk/rook.gd")
const RookResult = preload("res://rookframe/sdk/rook_result.gd")
const RookListResult = preload("res://rookframe/sdk/rook_list_result.gd")
const PublicIdentity = preload("res://rookframe/sdk/public_identity.gd")
const PublicIdentityResult = preload("res://rookframe/sdk/public_identity_result.gd")
const PublicIdentityListResult = preload("res://rookframe/sdk/public_identity_list_result.gd")
const Scene = preload("res://rookframe/sdk/scene.gd")
const SceneResult = preload("res://rookframe/sdk/scene_result.gd")
const ContentEntry = preload("res://rookframe/sdk/content_entry.gd")
const ContentEntryResult = preload("res://rookframe/sdk/content_entry_result.gd")
const ContentEntryListResult = preload("res://rookframe/sdk/content_entry_list_result.gd")
const Actors = preload("res://rookframe/sdk/actors.gd")
const PublicIdentities = preload("res://rookframe/sdk/public_identities.gd")
const SystemRecords = preload("res://rookframe/sdk/system_records.gd")
const Rooks = preload("res://rookframe/sdk/rooks.gd")
const DistanceResult = preload("res://rookframe/sdk/distance_result.gd")
const Scenes = preload("res://rookframe/sdk/scenes.gd")
const Content = preload("res://rookframe/sdk/content.gd")
const ContentKind = preload("res://rookframe/sdk/content_kind.gd")
const Windows = preload("res://rookframe/sdk/windows.gd")
const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
const TargetSnapshot = preload("res://rookframe/sdk/target_snapshot.gd")
const TargetSnapshotResult = preload("res://rookframe/sdk/target_snapshot_result.gd")
const Targeting = preload("res://rookframe/sdk/targeting.gd")
const ActorAccessEntry = preload("res://rookframe/sdk/actor_access_entry.gd")
const ActorAccessListResult = preload("res://rookframe/sdk/actor_access_list_result.gd")
const ActionLogText = preload("res://rookframe/sdk/action_log_text.gd")
const ActionLogDie = preload("res://rookframe/sdk/action_log_die.gd")
const ActionLogMessage = preload("res://rookframe/sdk/action_log_message.gd")
const ActionLogResult = preload("res://rookframe/sdk/action_log_result.gd")
const ActionLog = preload("res://rookframe/sdk/action_log.gd")
const DiceTerm = preload("res://rookframe/sdk/dice_term.gd")
const DiceRequest = preload("res://rookframe/sdk/dice_request.gd")
const DiceTermResult = preload("res://rookframe/sdk/dice_term_result.gd")
const DiceRollResult = preload("res://rookframe/sdk/dice_roll_result.gd")
const Dice = preload("res://rookframe/sdk/dice.gd")
const HumanThrowRequest = preload("res://rookframe/sdk/human_throw_request.gd")
const HumanThrowResult = preload("res://rookframe/sdk/human_throw_result.gd")
const SystemActions = preload("res://rookframe/sdk/system_actions.gd")
const ActorChange = preload("res://rookframe/sdk/actor_change.gd")
const SystemActionContext = preload("res://rookframe/sdk/system_action_context.gd")
const Announcement = preload("res://rookframe/sdk/announcement.gd")
const Announcements = preload("res://rookframe/sdk/announcements.gd")

func context() -> WorldContext:
	return WorldContext.new(_host.WorldContext())

var _world_data: WorldData
var world_data: WorldData:
	get:
		return _world_data

var _actors: Actors
var actors: Actors:
	get:
		return _actors

var _public_identities: PublicIdentities
var public_identities: PublicIdentities:
	get:
		return _public_identities

var _system_records: SystemRecords
var system_records: SystemRecords:
	get:
		return _system_records

var _rooks: Rooks
var rooks: Rooks:
	get:
		return _rooks

var _scenes: Scenes
var scenes: Scenes:
	get:
		return _scenes

var _content: Content
var content: Content:
	get:
		return _content

var _windows: Windows
var windows: Windows:
	get:
		return _windows

var _builder: UnavailableCapability
var builder: UnavailableCapability:
	get:
		return _builder

var _targeting: Targeting
var targeting: Targeting:
	get:
		return _targeting

var _dice: Dice
var dice: Dice:
	get:
		return _dice

var _system_actions: SystemActions
var system_actions: SystemActions:
	get:
		return _system_actions

var _action_log: ActionLog
var action_log: ActionLog:
	get:
		return _action_log

var _announcements: Announcements
var announcements: Announcements:
	get:
		return _announcements

signal world_changed
func _world_changed() -> void:
	world_changed.emit()

const SettingsScope = preload("res://rookframe/sdk/settings_scope.gd")
const Setting = preload("res://rookframe/sdk/setting.gd")
const TextSetting = preload("res://rookframe/sdk/text_setting.gd")
const SecretSetting = preload("res://rookframe/sdk/secret_setting.gd")
const SettingsRegistration = preload("res://rookframe/sdk/settings_registration.gd")
const SettingsValidation = preload("res://rookframe/sdk/settings_validation.gd")
const ToggleSetting = preload("res://rookframe/sdk/toggle_setting.gd")
const IntegerSetting = preload("res://rookframe/sdk/integer_setting.gd")
const NumberSetting = preload("res://rookframe/sdk/number_setting.gd")
const ObjectSetting = preload("res://rookframe/sdk/object_setting.gd")
const ArraySetting = preload("res://rookframe/sdk/array_setting.gd")
const TextListSetting = preload("res://rookframe/sdk/text_list_setting.gd")
const TextList = preload("res://rookframe/sdk/text_list.gd")
const IntegerListSetting = preload("res://rookframe/sdk/integer_list_setting.gd")
const IntegerList = preload("res://rookframe/sdk/integer_list.gd")
const SettingsValues = preload("res://rookframe/sdk/settings_values.gd")
const SettingsDraft = preload("res://rookframe/sdk/settings_draft.gd")
const SettingsCandidate = preload("res://rookframe/sdk/settings_candidate.gd")
const SettingsMigration = preload("res://rookframe/sdk/settings_migration.gd")
const Settings = preload("res://rookframe/sdk/settings.gd")
const SettingsView = preload("res://rookframe/sdk/settings_view.gd")
const SettingsViewDefinition = preload("res://rookframe/sdk/settings_view_definition.gd")

var _settings: Settings
var settings: Settings:
	get:
		return _settings

const IntegrationResult = preload("res://rookframe/sdk/integration_result.gd")
const TextResult = preload("res://rookframe/sdk/text_result.gd")
const BytesResult = preload("res://rookframe/sdk/bytes_result.gd")
const Clipboard = preload("res://rookframe/sdk/clipboard.gd")
const Files = preload("res://rookframe/sdk/files.gd")
const FileArea = preload("res://rookframe/sdk/file_area.gd")
const ScopedFile = preload("res://rookframe/sdk/scoped_file.gd")
const ScopedFolder = preload("res://rookframe/sdk/scoped_folder.gd")
const ResponseResult = preload("res://rookframe/sdk/response_result.gd")
const ServiceDefinition = preload("res://rookframe/sdk/service_definition.gd")
const HttpMethod = preload("res://rookframe/sdk/http_method.gd")
const RequestHeaders = preload("res://rookframe/sdk/request_headers.gd")
const Network = preload("res://rookframe/sdk/network.gd")
const NamedService = preload("res://rookframe/sdk/named_service.gd")
const PortraitResult = preload("res://rookframe/sdk/portrait_result.gd")
const FileSelectionResult = preload("res://rookframe/sdk/file_selection_result.gd")
const FolderSelectionResult = preload("res://rookframe/sdk/folder_selection_result.gd")
const ScopedStream = preload("res://rookframe/sdk/scoped_stream.gd")
const StreamResult = preload("res://rookframe/sdk/stream_result.gd")
const FileLocation = preload("res://rookframe/sdk/file_location.gd")
const InternalFileReference = preload("res://rookframe/sdk/internal_file_reference.gd")
const InternalFolderReference = preload("res://rookframe/sdk/internal_folder_reference.gd")
const AuthenticationProviderDefinition = preload("res://rookframe/sdk/authentication_provider_definition.gd")
const SecretResult = preload("res://rookframe/sdk/secret_result.gd")
const ProviderTokens = preload("res://rookframe/sdk/provider_tokens.gd")
const ProviderTokenResult = preload("res://rookframe/sdk/provider_token_result.gd")
const Secrets = preload("res://rookframe/sdk/secrets.gd")
const SecretArea = preload("res://rookframe/sdk/secret_area.gd")
const SecretEntry = preload("res://rookframe/sdk/secret_entry.gd")
const Authentication = preload("res://rookframe/sdk/authentication.gd")
const AccountStatus = preload("res://rookframe/sdk/account_status.gd")
const Account = preload("res://rookframe/sdk/account.gd")
const Browser = preload("res://rookframe/sdk/browser.gd")
const ServiceScope = preload("res://rookframe/sdk/service_scope.gd")
var _service_scope: ServiceScope

var _files: Files
var files: Files:
	get:
		return _files

var _clipboard: Clipboard
var clipboard: Clipboard:
	get:
		return _clipboard

var _network: Network
var network: Network:
	get:
		return _network

var _secrets: Secrets
var secrets: Secrets:
	get:
		return _secrets

var _authentication: Authentication
var authentication: Authentication:
	get:
		return _authentication

var _browser: Browser
var browser: Browser:
	get:
		return _browser

const ActorSummary = preload("res://rookframe/sdk/actor_summary.gd")

const ActorDefinitionView = preload("res://rookframe/sdk/actor_definition_view.gd")

const ActorPortraits = preload("res://rookframe/sdk/actor_portraits.gd")
const ActorPortraitResult = preload("res://rookframe/sdk/actor_portrait_result.gd")
var _portraits: ActorPortraits
var portraits: ActorPortraits:
	get:
		return _portraits

const CharacterHud = preload("res://rookframe/sdk/character_hud.gd")
const CharacterHudContext = preload("res://rookframe/sdk/character_hud_context.gd")
var _character_hud: CharacterHud
var character_hud: CharacterHud:
	get:
		return _character_hud

const Huds = preload("res://rookframe/sdk/huds.gd")
const HudContribution = preload("res://rookframe/sdk/hud_contribution.gd")
var _huds: Huds
var huds: Huds:
	get:
		return _huds
