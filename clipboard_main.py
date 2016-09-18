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

import clipboard

class Candidates:
    NONE, F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, CLEAR, KILL = range(13)

class GlobalData:

    def __init__(self):
        self.firstEnter = False
        self.ctrlDown = False
        self.currLock = Candidates.NONE
        self.keyboard = Controller()
        self.keyToEnum = self.buildDict()

    def buildDict(self):
        myDct = {}
        for i in range(1, 13):
            _str = "Key.f%d" % i
            myDct[_str] = i

        return myDct

    def clear(self):
        self.firstEnter = False
        self.ctrlDown = False
        self.currLock = Candidates.NONE

myGlobals = GlobalData()

def onPress(key):
    global myGlobals

    if not myGlobals.ctrlDown:
        if key == Key.ctrl:
            myGlobals.ctrlDown = True

    elif isFKey(key): # get the lock from F keys

        if myGlobals.currLock == Candidates.NONE: # lock available
            myGlobals.currLock = fKeyToValue(key)

        if myGlobals.currLock == Candidates.CLEAR:
            resetService()

    else:
        try:
            x = str(key)[2:3]
        except:
            pass

        if x == 'b':
            writeToClipboard()
        elif x == 'n':
            readFromClipboard()

    


    ### DEBUG ###
    if key == Key.enter:
        clearClipboard()
        return False

def onRelease(key):
    global myGlobals

    if myGlobals.currLock == Candidates.KILL:
        resetService()
        return False

    if key == Key.ctrl:
        myGlobals.ctrlDown = False
    elif isFKey(key):
        myGlobals.currLock = Candidates.NONE

def resetService():
    # Reset all constants and locks, prepare for exit
    global myGlobals
    myGlobals.clear()
    clearClipboard()
    
def clearClipboard():
    print "clear"

def writeToClipboard():
    global myGlobals

    myGlobals.keyboard.press(Key.ctrl)
    myGlobals.keyboard.press('c')
    myGlobals.keyboard.release('c')
    myGlobals.keyboard.release(Key.ctrl)
    # Tricky tricky! We just copied our data to the clipboard. Now let's store it!
    data = clipboard.paste()

    currBoard = myGlobals.currLock - 1
    print "write", currBoard

def readFromClipboard():
    global myGlobals
    currBoard = myGlobals.currLock - 1
    print "read", currBoard

    # put my data from lock into clipboard
    # clipboard.copy(data_object)

    myGlobals.keyboard.press(Key.ctrl)
    myGlobals.keyboard.press('v')
    myGlobals.keyboard.release(Key.ctrl)
    myGlobals.keyboard.release('v')

def isFKey(key):
    global myGlobals
    return str(key) in myGlobals.keyToEnum.keys()

def fKeyToValue(key):
    global myGlobals
    return myGlobals.keyToEnum[str(key)]

def main():
    time.sleep(1)
    global myGlobals
    myGlobals.clear()
    print "Launching clipboard service..."

    with Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()
    print "Returned to main thread."
    print "Exiting Service."

if __name__ == "__main__":
    # We will be calling this code from shell script
    main()