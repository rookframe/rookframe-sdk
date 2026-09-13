extends "res://rookframe/packages/bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb/sdk/window.gd"

const HeroData = preload("res://rookframe/packages/bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb/logic/hero_data.gd")
const TextField = preload("res://rookframe/ui/components/forms/text_field.gd")
@onready var actor_name: TextField = get_node("Layout/Body/Fields/ActorName")
@onready var journal_title: TextField = get_node("Layout/Body/Fields/JournalTitle")
@onready var status: Label = get_node("Layout/Status")
var selected_actor: SDK.ActorId
var selected_record: SDK.SystemRecordId

func ready() -> void:
	if sdk != null:
		refresh()
	show_actors()

func refresh() -> void:
	var actors: SDK.ActorListResult = sdk.actors.list()
	var records: SDK.SystemRecordListResult = sdk.system_records.list("journal")
	if not actors.ok:
		status.text = actors.message
		return
	if not records.ok:
		status.text = records.message
		return
	if selected_actor == null and not actors.items.is_empty():
		selected_actor = actors.items[0].id
	if selected_record == null and not records.items.is_empty():
		selected_record = records.items[0].id
	get_node("Layout/Body/Fields/ActorSummary").text = "No Actor selected"
	if selected_actor != null:
		var found: SDK.ActorResult = sdk.actors.read(selected_actor)
		if found.ok:
			var hero: HeroData = found.actor.data
			get_node("Layout/Body/Fields/ActorSummary").text = hero.display_name + " · HP " + str(hero.hit_points) + " · " + str(actors.items.size()) + " Actors"
	get_node("Layout/Body/Fields/JournalSummary").text = "No journal entry selected"
	if selected_record != null:
		var found: SDK.SystemRecordResult = sdk.system_records.read(selected_record)
		if found.ok:
			var data: Dictionary = found.system_record.data
			var title: String = data.get("title")
			get_node("Layout/Body/Fields/JournalSummary").text = title + " · " + str(records.items.size()) + " entries"
	get_node("Layout/Body/Fields/TrainActor").disabled = selected_actor == null
	get_node("Layout/Body/Fields/DeleteActor").disabled = selected_actor == null
	get_node("Layout/Body/Fields/SaveEntry").disabled = selected_record == null
	get_node("Layout/Body/Fields/DeleteEntry").disabled = selected_record == null

func create_actor() -> void:
	if actor_name.value.strip_edges().is_empty():
		status.text = "Enter a name before confirming Actor creation."
		return
	var definition: SDK.ContentReference = SDK.ContentReference.new(sdk.package_id(), "hero")
	var result: SDK.ActorResult = sdk.actors.create(definition, actor_name.value)
	if result.ok:
		selected_actor = result.actor.id
		refresh()
		status.text = "Actor saved. You have Owner access."
	else:
		status.text = result.message

func train_actor() -> void:
	if selected_actor == null:
		return
	var found: SDK.ActorResult = sdk.actors.read(selected_actor)
	if not found.ok:
		status.text = found.message
		return
	var hero: HeroData = found.actor.data
	hero.hit_points += 1
	var result: SDK.ActorResult = sdk.actors.update(selected_actor, hero)
	finish(result, "Training saved: +1 HP.")

func delete_actor() -> void:
	if selected_actor == null:
		return
	var result: SDK.OperationResult = sdk.actors.delete(selected_actor)
	if result.ok:
		selected_actor = null
	finish(result, "Actor deleted; its Rooks remain independent.")

func create_entry() -> void:
	if journal_title.value.strip_edges().is_empty():
		status.text = "Enter a journal title."
		return
	var result: SDK.SystemRecordResult = sdk.system_records.create("journal", {"title": journal_title.value.strip_edges()})
	if result.ok:
		selected_record = result.system_record.id
	finish(result, "Journal entry saved.")

func save_entry() -> void:
	if selected_record == null or journal_title.value.strip_edges().is_empty():
		status.text = "Select an entry and enter a journal title."
		return
	var result: SDK.SystemRecordResult = sdk.system_records.update(selected_record, {"title": journal_title.value.strip_edges()})
	finish(result, "Journal entry updated.")

func delete_entry() -> void:
	if selected_record == null:
		return
	var result: SDK.OperationResult = sdk.system_records.delete(selected_record)
	if result.ok:
		selected_record = null
	finish(result, "Journal entry deleted.")

func finish(result: SDK.OperationResult, message: String) -> void:
	if result.ok:
		refresh()
		status.text = message
	else:
		status.text = result.message

func show_actors() -> void:
	show_view(true)

func show_journal() -> void:
	show_view(false)

func show_view(actors: bool) -> void:
	get_node("Layout/Body/Fields/ActorHeading").visible = actors
	get_node("Layout/Body/Fields/ActorName").visible = actors
	get_node("Layout/Body/Fields/CreateActor").visible = actors
	get_node("Layout/Body/Fields/ActorSummary").visible = actors
	get_node("Layout/Body/Fields/TrainActor").visible = actors
	get_node("Layout/Body/Fields/DeleteActor").visible = actors
	get_node("Layout/Body/Fields/JournalHeading").visible = not actors
	get_node("Layout/Body/Fields/JournalTitle").visible = not actors
	get_node("Layout/Body/Fields/CreateEntry").visible = not actors
	get_node("Layout/Body/Fields/JournalSummary").visible = not actors
	get_node("Layout/Body/Fields/SaveEntry").visible = not actors
	get_node("Layout/Body/Fields/DeleteEntry").visible = not actors
	get_node("Layout/Views/Actors").disabled = actors
	get_node("Layout/Views/Journal").disabled = not actors
