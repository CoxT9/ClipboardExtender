"""
 - This code uses a small package called Pynut to handle keydown/keyup events. 
 Credits to Moses Palmer (https://github.com/moses-palmer/) for the underlying code.

 - This code uses a clipboard module called Clipboard for under-the-hood clipboard read/write
 Credits to Terry Yin (https://github.com/terryyin) for the underlying code.

 The goal of this project is an augmented approach to the standard clipboard.
 The end result will be a background process that provides 10 different clipboards (F1,10)
 The tool will also provide the ability to clear all boards (F11) or end the service (F12)
 Copy is ctrl-f#-b, Paste is ctrl-f#-n, clear is ctrl-f11, kill is ctrl-f12.
 Note that this tool is ultimately intended to be platform-agnostic

 - an issue that seems unavoidable is that just about any keyboard combination has some conflicting funcationality,
 this could be something small and annoying like ctrl-f, or something disastrous like alt-f4. Ideal keyboard usage
 may still be explored, but the first goal is a working prototype
"""

# Currently able to read in (copy in) highlighted text or even a file, it looks like.
# Next: add structure(s) for storing 10 different clipboard buffers
# Then plug in clipboard and storage in read/write functions
# test, test, test (still in terminal)
# move to have shell script that launches py script

import time
import sys
from pynput.keyboard import Key, Controller, Listener

import pyperclip

class Utilities:

    class FunctionKeys:
        NONE, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, CLEAR, KILL = range(13)

    def __init__(self):
        self.ctrlDown = False
        self.currLock = self.FunctionKeys.NONE
        self.keyboard = Controller()
        self.keyToEnum = self.buildDict()
        self.boards = [None] * 10

    def buildDict(self):
        myDct = {}
        for i in range(1, 13):
            _str = "Key.f%d" % i
            myDct[_str] = i

        return myDct

    def clear(self):
        self.ctrlDown = False
        self.currLock = self.FunctionKeys.NONE
        self.boards = [None] * 10

    def sendCopy(self):
        print "...ctrlc"
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('c')
        self.keyboard.release('c')
        self.keyboard.release(Key.ctrl)

        # hack: do it twice
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('c')
        self.keyboard.release('c')
        self.keyboard.release(Key.ctrl)

    def sendPaste(self):
        print "...ctrlv"
        self.keyboard.press(Key.ctrl)
        self.keyboard.press('v')
        self.keyboard.release(Key.ctrl)
        self.keyboard.release('v')

class ClipboardManager:

    def __init__(self):
        self.utils = Utilities()

    def onPress(self, key):
        if not self.utils.ctrlDown:
            if key == Key.ctrl:
                self.utils.ctrlDown = True
        elif self.isFKey(key): # get the lock from F keys
            if self.utils.currLock == self.utils.FunctionKeys.NONE: # lock available
                self.utils.currLock = self.fKeyToValue(key)

            if self.utils.currLock == self.utils.FunctionKeys.CLEAR:
                self.utils.clear()

        else:
            try:
                char = str(key)[2:3]
            except:
                char = 'x'

            if char == 'b':
                self.writeToClipboard()
            elif char == 'm':
                self.readFromClipboard()

        ### DEBUG ###
        if key == Key.enter:
            self.utils.clear()
            return False

    def onRelease(self, key):
        if self.utils.currLock == self.utils.FunctionKeys.KILL:
            self.utils.clear()
            return False

        if key == Key.ctrl:
            self.utils.ctrlDown = False
        elif self.isFKey(key):
            self.utils.currLock = self.utils.FunctionKeys.NONE

    def writeToClipboard(self): # Write to board, read from highlight
        self.utils.sendCopy()
        data = pyperclip.paste()
        print data, " is copy data"
        currBoard = self.utils.currLock - 1
        print "write", currBoard
        self.utils.boards[currBoard] = data
        print self.utils.boards[currBoard], "is the conf data"

    def readFromClipboard(self): # Read from board, write to highlight
        currBoard = self.utils.currLock - 1
        print "read", currBoard
        print self.utils.boards[currBoard]
        data = self.utils.boards[currBoard]
        if data != None:
            print "copy"
            pyperclip.copy(data)

        self.utils.sendPaste()

    def isFKey(self, key):
        return str(key) in self.utils.keyToEnum.keys()

    def fKeyToValue(self, key):
        return self.utils.keyToEnum[str(key)]

def main():
    time.sleep(1)
    mgr = ClipboardManager()
    print "Launching clipboard service..."

    with Listener(on_press=mgr.onPress, on_release=mgr.onRelease) as listener:
        listener.join()
    print "Returned to main thread."
    print "Exiting Service."

if __name__ == "__main__":
    # We will be calling this code from shell script
    main()