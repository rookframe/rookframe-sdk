# Integration example

A separate ordinary optional Package for SDK 0.8.0 (Edition 2029 revision 1).
It uses authored scenes, generated concrete SDK types and the independently
pinned UI Kit. It imports no application assembly or private host API. Calendar
does not depend on this example and has no provider account requirement.

Install gd-plug's bootstrap at `addons/gd-plug/plug.gd` as described in the
[SDK README](../../README.md), then run from this directory:

```sh
/path/to/godot --headless --path . --script plug.gd install
python3 addons/rookframe_sdk/rookframe_authoring.py check --project . --godot /path/to/godot
python3 addons/rookframe_sdk/rookframe_authoring.py build --project . --godot /path/to/godot
```

Import the resulting archive through Manager and include it alongside one
System Extension. Open **Integration example** from the left Rail.

- Save/read a note in this Package's User files, choose an existing file or
  folder, read immutable welcome content, or decode a selected PNG/JPEG/WebP portrait.
- Call the named service, read one bounded stream chunk and close it, download
  an internal file, or upload the selected internal file.
- Use Package Settings to enter a protected API key or World key. Provider
  account settings expose host-owned Sign in, Refresh and Clear actions.
- Sign in from the scene or settings, then call the service. A bound typed account supplies
  credentials and preflight expiry refresh to the checked service. The scene awaits
  the completed result without a polling loop. Status text never displays credentials or response bodies.

The shipped `.invalid` service/provider URLs deliberately require configuration.
File controls work independently. To connect your deployment, edit the Package's
`services.json` and `authentication.json`, register a compatible native client or
Publisher transfer backend, then rebuild through the same checks. The sample
expects GET `identity`, streaming GET `messages`, downloadable GET `ok`, and
POST `upload`. A deployment may split these endpoints into separate declarations.
Neither example ships client secrets or embeds a production provider registration.

A local controlled companion must be configured by the device operator in
`user://package-service-connections.json`, outside Package storage. Entries name
the original World Address and Package ID and contain `services` and optional
`authentication` arrays in the declaration formats. A paired destination additionally
requires `companionAddress` and `companionCertificateSha256`; changing the port
alone does not grant access. Restart the World after changing host configuration.
See the [integration API](../../API.md#checked-integrations--edition-2029-revision-1)
for lifetimes, protected storage, provider responsibilities and explicit failures.

This project configures desktop export. The responsive scene and host settings
can use the existing phone/tablet shell profiles, but this example does not certify
mobile hardware permissions or a live third-party provider.
