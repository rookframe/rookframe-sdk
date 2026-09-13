extends "res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/sdk/window.gd"

const API: SDK.ServiceDefinition = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/api.tres")
const IDENTITY: SDK.AuthenticationProviderDefinition = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/identity.tres")
const API_KEY: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/api_key.tres")
const ACCOUNT: SDK.SecretSetting = preload("res://rookframe/packages/9f64487d-5a09-48e0-8bdf-8071dd9ef882/logic/account.tres")
const TextArea = preload("res://rookframe/ui/components/forms/text_area.gd")

@onready var note: TextArea = get_node("Body/Fields/Note")
@onready var status: Label = get_node("Status")
var request: SDK.RequestOperation
var transfer: SDK.IntegrationOperation
var opening_stream: SDK.StreamOperation
var reading_stream: SDK.BytesOperation
var stream: SDK.ScopedStream
var selecting_file: SDK.FileSelection
var selecting_folder: SDK.FolderSelection
var authentication: SDK.AuthenticationOperation
var selected_file: SDK.ScopedFile
var selected_folder: SDK.ScopedFolder
var portrait_selection: bool = false

func ready() -> void:
	if sdk == null:
		status.text = "Open this Package in a Rookframe World to use integrations."
	else:
		selected_file = sdk.files.user.file("notes/example.txt")

func can_start() -> bool:
	if sdk == null:
		status.text = "Open this Package in a Rookframe World."
		return false
	if request != null or transfer != null or opening_stream != null or reading_stream != null or selecting_file != null or selecting_folder != null or authentication != null:
		status.text = "Finish the current operation first."
		return false
	return true

func show_result(result: SDK.IntegrationResult, success: String) -> void:
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
	if can_start():
		portrait_selection = false
		selecting_file = sdk.files.user.select_file()

func choose_portrait() -> void:
	if can_start():
		portrait_selection = true
		selecting_file = sdk.files.user.select_file()

func choose_folder() -> void:
	if can_start():
		selecting_folder = sdk.files.user.select_folder()

func call_service() -> void:
	if not can_start():
		return
	var headers: SDK.RequestHeaders = SDK.RequestHeaders.new()
	var key: SDK.SecretResult = sdk.secrets.user.setting(API_KEY).read()
	if key.ok and key.found:
		headers.api_key = key.text
	var account: SDK.ProviderTokenResult = sdk.secrets.user.setting(ACCOUNT).read_tokens()
	if account.ok and account.found:
		headers.authorization = account.tokens.token_type + " " + account.tokens.access_token
	request = sdk.network.service(API).request("identity", SDK.HttpMethod.Value.GET, "", headers)
	status.text = "Requesting the configured service…"

func read_stream() -> void:
	if can_start():
		opening_stream = sdk.network.service(API).open_stream("messages")
		status.text = "Opening a bounded message stream…"

func download_file() -> void:
	if can_start():
		transfer = sdk.network.service(API).download("ok", sdk.files.user.file("download.txt"))
		status.text = "Downloading to this Package's internal files…"

func upload_file() -> void:
	if can_start():
		request = sdk.network.service(API).upload("upload", selected_file)
		status.text = "Uploading the selected internal file…"

func sign_in() -> void:
	if can_start():
		authentication = sdk.authentication.provider(IDENTITY).sign_in(sdk.secrets.user.setting(ACCOUNT))
		status.text = "Confirm to open the provider in your browser."

func refresh_account() -> void:
	if can_start():
		transfer = sdk.authentication.provider(IDENTITY).refresh(sdk.secrets.user.setting(ACCOUNT))
		status.text = "Refreshing credentials…"

func account_status() -> void:
	if not can_start():
		return
	var account: SDK.ProviderTokenResult = sdk.secrets.user.setting(ACCOUNT).read_tokens()
	show_result(account, "Account credentials are stored." if account.found else "No account credentials stored. Use Sign in or Package Settings.")

func _process(_delta: float) -> void:
	if request != null:
		var result: SDK.ResponseResult = request.poll()
		if result.ready:
			show_result(result, "Service returned HTTP %d." % result.status)
			request = null
	if transfer != null:
		var result: SDK.IntegrationResult = transfer.poll()
		if result.ready:
			show_result(result, "Operation completed.")
			transfer = null
	if opening_stream != null:
		var result: SDK.StreamResult = opening_stream.poll()
		if result.ready:
			opening_stream = null
			if result.ok:
				stream = result.stream
				reading_stream = stream.read(1024)
			else:
				show_result(result, "")
	if reading_stream != null:
		var result: SDK.BytesResult = reading_stream.poll()
		if result.ready:
			show_result(result, "Read %d bytes from the stream, then closed it." % result.data.size())
			stream.close()
			stream = null
			reading_stream = null
	if selecting_file != null:
		var result: SDK.FileSelectionResult = selecting_file.poll()
		if result.ready:
			selecting_file = null
			if result.ok:
				selected_file = result.file
				if portrait_selection:
					var portrait: SDK.PortraitResult = selected_file.read_portrait()
					get_node("Body/Fields/Portrait").texture = portrait.texture
					show_result(portrait, "Portrait decoded and fitted to 512 × 512.")
				else:
					show_result(result, "File selected. Read or upload uses this scoped file only.")
			else:
				show_result(result, "")
	if selecting_folder != null:
		var result: SDK.FolderSelectionResult = selecting_folder.poll()
		if result.ready:
			selecting_folder = null
			if result.ok:
				selected_folder = result.folder
			show_result(result, "Folder selected. Save note writes example.txt within it.")
	if authentication != null:
		var result: SDK.AuthenticationResult = authentication.poll()
		if result.ready:
			show_result(result, "Signed in. Raw provider tokens are available to this Package's checked requests.")
			authentication = null
		elif result.phase == SDK.AuthenticationResult.Phase.BROWSER:
			status.text = "Finish in your browser. The launched flow may complete after leaving this World."
