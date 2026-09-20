extends "res://rookframe/packages/dddddddd-dddd-4ddd-8ddd-dddddddddddd/sdk/window.gd"

func share_tip() -> void:
	get_node("ShareTip").disabled = true
	var message := SDK.ActionLogMessage.new("A table tip")
	message.text = [SDK.ActionLogText.new("Use Targeting to show the table which Rook your action concerns.")]
	var result: SDK.ActionLogResult = await sdk.action_log.publish(message)
	get_node("ShareTip").disabled = false
	if not result.ok:
		var notice := SDK.FeedbackMessage.new()
		notice.title = "Tip could not be shared"
		notice.message = result.message
		sdk.feedback.warning(notice)
