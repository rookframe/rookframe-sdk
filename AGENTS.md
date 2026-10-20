# SDK source

Maintain optional directly usable typed GDScript in `rookframe/sdk/`. Package
authors may install it with the Development Plugin menu or their chosen dependency
manager. No Package kind requires this library or the UI Kit. Keep runtime
behavior and API compatibility in Rookframe's C# API. All Package authoring tools,
including checking, building, media and publication, belong exclusively in
`rookframe-development-plugin`. Do not add editor tooling or authoring bootstrap
scripts to this SDK.

Verify changed SDK calls with stock Godot and the matching application before
publishing. Reuse the existing author project and Development World. Keep research
and generated evidence outside this repository.
