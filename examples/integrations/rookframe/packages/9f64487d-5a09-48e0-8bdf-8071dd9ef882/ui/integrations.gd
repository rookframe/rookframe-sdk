extends "res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/sdk/window.gd"

const API: SDK.ServiceDefinition = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/api.tres")
const API_KEY: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/api_key.tres")
const ACCOUNT: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/account.tres")
const TextArea = preload("res://rookframe/ui/components/forms/text_area.gd")

@onready var note: TextArea = get_node("Body/Fields/Note")
@onready var status: Label = get_node("Status")
var service: SDK.NamedService
var account: SDK.Account
var busy: bool = false
var selected_file: SDK.ScopedFile
var selected_folder: SDK.ScopedFolder

func ready() -> void:
	if sdk == null:
		status.text = "Open this Package in a Rookframe World to use integrations."
	else:
		selected_file = sdk.files.user.file("notes/example.txt")
		service = sdk.network.service(API)
		account = sdk.authentication.account(ACCOUNT)

func can_start() -> bool:
	if sdk == null:
		status.text = "Open this Package in a Rookframe World."
		return false
	if busy:
		status.text = "Finish the current operation first."
		return false
	return true

func show_result(result: SDK.IntegrationResult, success: String) -> void:
	busy = false
	status.text = success if result.ok else result.message

func save_note() -> void:
	if not can_start():
		return
	selected_file = selected_folder.file("example.txt") if selected_folder != null else sdk.files.user.file("notes/example.txt")
	show_result(selected_file.write_text(note.value), "Note saved in this Package's files on this device.")

func read_note() -> void:
	if not can_start():
		return
	var result: SDK.TextResult = selected_file.read_text()
	if result.ok:
		note.value = result.text
	show_result(result, "Read the selected internal file.")

func read_content() -> void:
	if not can_start():
		return
	var result: SDK.TextResult = sdk.files.package.file("data/welcome.json").read_text()
	show_result(result, result.text)

func choose_file() -> void:
	if not can_start():
		return
	busy = true
	var result: SDK.FileSelectionResult = await sdk.files.user.select_file()
	if result.ok:
		selected_file = result.file
	show_result(result, "File selected. Read or upload uses this scoped file only.")

func choose_portrait() -> void:
	if not can_start():
		return
	busy = true
	var result: SDK.FileSelectionResult = await sdk.files.user.select_file()
	if not result.ok:
		show_result(result, "")
		return
	selected_file = result.file
	var portrait: SDK.PortraitResult = selected_file.read_portrait()
	if portrait.ok:
		get_node("Body/Fields/Portrait").texture = portrait.texture
	show_result(portrait, "Portrait decoded and fitted to 512 × 512.")

func choose_folder() -> void:
	if not can_start():
		return
	busy = true
	var result: SDK.FolderSelectionResult = await sdk.files.user.select_folder()
	if result.ok:
		selected_folder = result.folder
	show_result(result, "Folder selected. Save note writes example.txt within it.")

func call_service() -> void:
	if not can_start():
		return
	busy = true
	status.text = "Requesting the configured service…"
	var headers: SDK.RequestHeaders = SDK.RequestHeaders.new()
	var key: SDK.SecretResult = sdk.secrets.user.setting(API_KEY).read()
	if key.ok and key.found:
		headers.api_key = key.text
	var client: SDK.NamedService = sdk.network.service(API, account)
	var result: SDK.ResponseResult = await client.request("identity", SDK.HttpMethod.Value.GET, "", headers)
	show_result(result, "Service returned HTTP %d." % result.status)

func read_stream() -> void:
	if not can_start():
		return
	busy = true
	var opened: SDK.StreamResult = await service.open_stream("messages")
	if not opened.ok:
		show_result(opened, "")
		return
	var chunk: SDK.BytesResult = await opened.stream.read(1024)
	opened.stream.close()
	show_result(chunk, "Read %d bytes from the stream, then closed it." % chunk.data.size())

func download_file() -> void:
	if not can_start():
		return
	busy = true
	var result: SDK.IntegrationResult = await service.download("ok", sdk.files.user.file("download.txt"))
	show_result(result, "Downloaded to this Package's internal files.")

func upload_file() -> void:
	if not can_start():
		return
	busy = true
	var result: SDK.ResponseResult = await service.upload("upload", selected_file)
	show_result(result, "Upload returned HTTP %d." % result.status)

func sign_in() -> void:
	if not can_start():
		return
	busy = true
	status.text = "Confirm and finish signing in with your browser."
	var result: SDK.IntegrationResult = await account.sign_in()
	show_result(result, "Signed in. Requests use this account's current credentials.")

func refresh_account() -> void:
	if not can_start():
		return
	busy = true
	var result: SDK.IntegrationResult = await account.refresh()
	show_result(result, "Refreshed account credentials.")

func account_status() -> void:
	if not can_start():
		return
	var result: SDK.AccountStatus = account.status()
	if not result.ok:
		show_result(result, "")
	elif result.state == SDK.AccountStatus.State.SIGNED_OUT:
		status.text = "No account credentials stored. Use Sign in or Package Settings."
	elif result.state == SDK.AccountStatus.State.EXPIRED:
		status.text = "Credentials expired. The next request will refresh this account."
	else:
		status.text = "Account credentials are stored."
