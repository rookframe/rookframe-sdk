# Package forms and Edition conformance

These three small, ordinary author projects complement the separate Calendar repository.
Install the SDK and UI Kit from each project's exact pins using the normal gd-plug bootstrap
and commands in the SDK README. Run `check` and `build` in each project and publish each release before application QA.
Install through Manager using the public Manifest URL; invited Players acquire the
World’s required releases automatically. Local archive imports are prohibited for QA.
Catalogue listing is optional. Select the published Packages needed by the World.

- **Workshop System:** executable Edition 2029 revision 4; typed selected-Rook and System-only Actor Creation
  slots, native Actor-list presentation hooks, dedicated Actor creation and inspection windows, Actor Definitions and typed HeroData Resources. Confirming creates an independent Actor; Train queries its current data, adds one HP, and submits an update. A separate World journal rail entry creates, updates and deletes journal System Records.
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

Open Actors → Create Actor for the creation form. Confirm two names to observe
independent Actors in the native list. Click a row to inspect and train that
Actor; the Rook's contextual Inspect action opens its linked Actor through the
same SDK Actor-window contract. World journal has its own rail entry.
Delete actions remove only their selected record. Actor creation never places a Rook.
The sample's `workshop-actor-v1` contract uses `HeroData` with a name and hit points;
that schema belongs to this System, not to Rookframe.

Workshop also supplies a Presentation-specific typed SettingsView. Its personal
heading uses restart-local and its shared heading uses restart-world. Edit the
custom form and Save; the host explains the restart before a deliberate second
Save recreates the activation/session. Calendar's ordinary User date-display
preference and GM World title exercise live settings without supplemental features.

For remote action QA, install Workshop System and Tabletop Pieces on the GM endpoint
using their public Manifest URLs. Select those releases for the World so invited
Players acquire the exact same published releases automatically.
Create an Actor explicitly on the Player endpoint, then Train to calculate and
submit +1 HP. On the GM endpoint open the Actor row, then its Access tab to grant
Viewer, Owner, and None. Viewer shows VIEW ONLY; None closes the Actor sheet while the Actor and linked Rooks remain. Point at a Rook and press T on desktop; the Workshop displays the accepted count. The target snapshot is
awaited before training. Named cursors and targets belong to each active Session.
Journal mutations remain GM-only, and Package World Data remains Authority-only.

Published releases for the remote action QA World:

- [Workshop System 0.11.0](https://github.com/rookframe/rookframe-fixtures/releases/download/v0.11.0/Workshop-System-0.11.0.json)
- [Tabletop Pieces 0.9.0](https://github.com/rookframe/rookframe-fixtures/releases/download/v0.9.0/Tabletop-Pieces-0.9.0.json)
