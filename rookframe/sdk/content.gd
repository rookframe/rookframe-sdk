extends RefCounted
const OperationResult = preload("res://rookframe/sdk/operation_result.gd")


const WorldCapability = preload("res://rookframe/sdk/world_capability.gd")
const ContentReference = preload("res://rookframe/sdk/content_reference.gd")
const ContentEntryResult = preload("res://rookframe/sdk/content_entry_result.gd")
const ContentEntryListResult = preload("res://rookframe/sdk/content_entry_list_result.gd")
const ContentKind = preload("res://rookframe/sdk/content_kind.gd")

var _host: Object
func _init(host: Object) -> void:
	_host = host

func list(kind: ContentKind.Value = ContentKind.Value.ALL) -> ContentEntryListResult:
	return ContentEntryListResult.new(_host.ListContent(kind))
func read(reference: ContentReference) -> ContentEntryResult:
	return ContentEntryResult.new(_host.ReadContent(reference.package_id, reference.local_id))

## Render an available Miniature into this Package's authored UI placeholder.
func preview_miniature(reference: ContentReference, target: Control) -> OperationResult:
	return OperationResult.new(_host.PreviewMiniature(reference.package_id, reference.local_id, target))
