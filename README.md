# ClipboardExtender
A control-group inspired approach to making clipboards great again

This project was started at Hack The North 2016.

The intention of this project is to extend the current utility of the unix clipboard. I used "control groups" to make this happen.

Control-groups are from RTS games, where ctrl-# is used to read from/write to a specific group. # is a single integer 0 <= 9. 

Therefore, this project provides 10 seperate clipboards, each accessed by the corresponding numerical digit.

Ctrl+F# (1 through 10) provides access to a different clipboard. Ctrl-F#-b will copy and Ctrl-F#-m will paste. Ctrl-F11 will clear all clipboard and Ctrl-F12 will kill the process.

Use the .sh file provided to run the script without a console window.

This script works for Ubuntu with text in clipboards. 10 different text entries can be stored.
