#!C:\Python27\python.exe
# coding=utf-8

# a simple Tkinter number guessing game
# shows how to create a window, an entry, a label, a button,
# a button mouse click response, and how to use a grid for layout

import random
try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk

def click():
    """the mouse click command response"""
    global rn
    # get the number from the entry area
    num = int(enter1.get())
    # check it out
    if num > rn:
        label2['text'] = str(num) + " guessed too high!"
    elif num < rn:
        label2['text'] = str(num) + " guessed too low!"
    else:
        s1 = str(num) + " guessed correctly!"
        s2 = "\n Let's start a new game!"
        label2['text'] = s1 + s2
        # pick a new random number
        rn = random.randrange(1, 11)
    enter1.delete(0, 2)


# create the window and give it a title
root = tk.Tk()
root.title("Heidi's Guess A Number Game")

# pick a random integer from 1 to 10
rn = random.randrange(1, 11)

# let the user know what is going on
label1 = tk.Label(root, text="Guess a number between 1 and 10 -->")
# layout this label in the specified row and column of the grid
# also pad with spaces along the x and y direction
label1.grid(row=1, column=1, padx=10, pady=10)

# this your input area
enter1 = tk.Entry(root, width=5, bg='yellow')
enter1.grid(row=1, column=2, padx=10)
# put the cursor into the entry field
enter1.focus()

# action button, right-click it to execute command
button1 = tk.Button(root, text=" Press to check the guess ",
                    command=click)
button1.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

# the result displays here
label2 = tk.Label(root, text="", width=50)
label2.grid(row=3, column=1, columnspan=2, pady=10)

# start the mouse/keyboard event loop
root.mainloop()

