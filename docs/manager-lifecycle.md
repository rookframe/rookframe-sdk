# Package lifecycle and typed authorship

Manager installs exact `.rookpackage` releases. Opening a World creates a fresh
runtime from its accepted exact selection. Use the generated SDK types for the
Package implementation and presentation: `SDK.DataResult`, `SDK.OperationResult`,
`SDK.WorldContext`, typed settings descriptors, `Rail`, `WindowButton`, and
`ExtensionSurface`. Register authored resources through `sdk.rails.left.push(...)`;
Rookframe owns binding, opening, mounting and cleanup.

An update or repair does not provide a live runtime adoption callback. Temporary
helpers read fresh canonical values through `sdk.world_data.read()` and submit
one coherent value through `sdk.world_data.replace(...)`. They must not maintain
a second persistent model or synchronize a Node tree with stored data.

| Manager action | Author-visible consequence |
| --- | --- |
| Select a new release / Update All | The next activation receives the accepted release and retained World data/settings. Optional enabled state is preserved. |
| Disable / re-enable | Disabled code does not run. Its exact selection, World data and settings remain retained. |
| Exact repair | Restores the retained Manifest and fingerprint; the next activation sees the same retained data. |
| Package Deletion | Removes the optional selection and its World data/settings. Selecting it again starts without that data. |
| Uninstall | Blocked while any local World selects the exact version, including disabled entries. Its User settings and protected destinations are removed by Rookframe. |

A later activation failure keeps the accepted selection current. Manager offers
explicit repair, compatible release selection and optional disable. A Package
must interpret retained data safely and return a useful diagnostic if it cannot.
It must not silently reset unreadable data on startup.

Build once and keep the immutable archive for exact repair. Rebuilding the same
Manifest version creates a fresh build identity and requires installation-wide
replacement review. Increment the version for an ordinary update and retain the
original archive. Public Manifest bytes must match the embedded Manifest exactly.
No credentials, mirror or alternate release substitutes for an unavailable exact source.

The [Calendar example](https://github.com/rookframe/rookframe-calendar/blob/main/docs/manager-lifecycle.md)
exercises this contract with a Gregorian date and dated notes. Manager file
selection, drop and OS open-with are host inputs; no public SDK install, raw
Godot mount or operating-system adapter API is needed by a Package.
