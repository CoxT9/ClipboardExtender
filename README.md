# ClipboardExtender
A control-group inspired approach to expanding the clipboard utility

This project was started at Hack The North 2016.

The intention of this project is to extend the current utility of the unix clipboard. A control-group approach is proposed.

Control-groups are inspired from RTS games, where ctrl-F# is used to read from/write to a specific group. # is a single integer 0 <= 10. F11 clears the clipboard and F12 ends the service. 

Therefore, this project aims to provide 10 seperate clipboards, each accessed by the corresponding numerical digit.

This project is currently geared towards Unix systems ( python can be used both for clipboard management, keyboard events and developing a unix daemon ).

Future: Windows application, stack-based clipboard, examination of other python libraries or alternatives to python entirely, more user customisability (ie: hotkey management for F or even CTRL keys)
