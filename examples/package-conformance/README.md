# Package forms and Edition conformance

These three small, ordinary author projects complement the separate Calendar repository.
Install the SDK and UI Kit from each project's exact pins using the normal gd-plug bootstrap
and commands in the SDK README. Run `check` and `build` in each project, import the outputs
through Manager, and select Workshop System, Tabletop Pieces, Table Help and Calendar.

- **Workshop System:** executable Edition 2028; typed selected-Rook and System-only Actor Creation
  slots, Package UI Root, and structured feedback. It owns no game-specific Actor schema.
- **Tabletop Pieces:** data-only Edition 2027; semantic Miniature, Prop, Surface Finish and Wall Style
  entries. No Implementation, Presentation or Settings callbacks run.
- **Table Help:** Presentation-only Edition 2027; one responsive Package UI Root contribution,
  with no Implementation or Package Settings.
- **Calendar:** independent executable Edition 2027 optional Package in `rookframe/rookframe-calendar`;
  its draft date/note workflow and three Presentations are maintained there.

The optional examples use direct Workshop System compatibility only. They do not load or call
one another. Calendar remains System-neutral. Every profile and every unused source is checked
by production admission. These examples use the independently pinned public UI Kit without
introducing another Kit release or copying it into a built Package.
