# Third-party notices

The distributed nonexecuting GDScript checker uses
[Tree-sitter 0.26.0](https://github.com/tree-sitter/tree-sitter/tree/v0.26.0)
and [tree-sitter-gdscript 6.1.0](https://github.com/PrestonKnopp/tree-sitter-gdscript/tree/v6.1.0),
both under the MIT license. The checker distribution includes `tree-sitter.LICENSE`
and `tree-sitter-gdscript.LICENSE`, plus `unicode.LICENSE` for the Unicode code
included in the Tree-sitter runtime. The source inventory and local Godot grammar
patch are retained in Rookframe's `native/gdscript-parser/` directory.

The UI Kit is acquired separately and retains its own notices and asset licenses.
The editor's dependency installer acquires gd-plug at commit
`209276d1f00d14b49b74403d9839f29598e9a8eb`, including its upstream MIT license.
The Calendar example also retains its bootstrap license. Neither bootstrap is
bundled into a Package archive.
