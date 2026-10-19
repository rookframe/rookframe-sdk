extends Resource

const FeedbackAction = preload("res://rookframe/sdk/feedback_action.gd")
@export var title: String
@export_multiline var message: String
@export var actions: Array[FeedbackAction] = []
