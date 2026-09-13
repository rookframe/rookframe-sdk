# Package forms and Edition conformance

These three small, ordinary author projects complement the separate Calendar repository.
Install the SDK and UI Kit from each project's exact pins using the normal gd-plug bootstrap
and commands in the SDK README. Run `check` and `build` in each project, import the outputs
through Manager, and select Workshop System, Tabletop Pieces, Table Help and Calendar.

- **Workshop System:** executable Edition 2028; typed selected-Rook and System-only Actor Creation
  slots, a managed Workshop window, Actor Definitions and typed HeroData Resources. Confirming creates an independent Actor; Train queries its current data, adds one HP, and submits an update. The same window creates, updates and deletes journal System Records.
- **Tabletop Pieces:** data-only Edition 2027; semantic Miniature, Prop, Surface Finish and Wall Style
  entries. No Implementation, Presentation or Settings callbacks run.
- **Table Help:** Presentation-only Edition 2027; one responsive Package UI Root contribution,
  with no Implementation or Package Settings.
- **Calendar:** independent executable Edition 2027 optional Package in `rookframe/rookframe-calendar`;
  its persisted Gregorian date/note workflow and three Presentations are maintained there.

The optional examples use direct Workshop System compatibility only. They do not load or call
one another. Calendar remains System-neutral. The complete shared artifact and every unused source is checked
by production admission. These examples use the independently pinned public UI Kit without
introducing another Kit release or copying it into a built Package.

Open Actors → Create Actor for the Workshop. Confirm two names to observe distinct
Actors, train the selected Actor, and create a journal entry. Close/leave/reopen the
World and open the Workshop again; it queries saved Actors and journal entries.
Delete actions remove only their selected record. Actor creation never places a Rook.
The sample's `workshop-actor-v1` contract uses `HeroData` with a name and hit points;
that schema belongs to this System, not to Rookframe.

Workshop also supplies a Presentation-specific typed SettingsView. Its personal
heading uses restart-local and its shared heading uses restart-world. Edit the
custom form and Save; the host explains the restart before a deliberate second
Save recreates the activation/session. Calendar's ordinary User date-display
preference and GM World title exercise live settings without supplemental features.
