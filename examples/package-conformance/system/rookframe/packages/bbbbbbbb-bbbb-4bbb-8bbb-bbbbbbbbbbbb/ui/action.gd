extends "res://rookframe/packages/bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb/sdk/window.gd"

func activate() -> void:
	var message: SDK.FeedbackMessage = SDK.FeedbackMessage.new()
	message.title = "Actor tools"
	message.message = "Actor tools are not connected in this example."
	sdk.feedback.notice(message)
