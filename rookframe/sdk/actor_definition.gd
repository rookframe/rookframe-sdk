extends Resource

## Override to calculate independent Actor data from a human's submitted choices.
## Rookframe executes this declared Content and owns identity, access and persistence.
func create_data(choices: Variant) -> Variant:
	return choices

## Override when this definition needs the owning Package's compiled data.
## The content reader is valid only during this callback.
func create_data_with_content(choices: Variant, _content: RefCounted) -> Variant:
	return create_data(choices)
