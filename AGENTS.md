# SDK source

Maintain directly usable typed GDScript in `rookframe/sdk/`. Package developers
install these files with gd-plug and use them; they never generate or compile the
SDK. Keep behavior and API compatibility in Rookframe's C# API. Keep editor
integration in `rookframe-development-plugin`. Package tooling here delegates
checking to the installed Rookframe application.

Run the Python tests and verify changed SDK calls with stock Godot and the matching
application before publishing. Reuse the existing author project and Development
World for native checks. Keep research and generated evidence outside this repository.
