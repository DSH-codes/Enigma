
import tkinter as tk

from tkinter import messagebox as mb

from tkinter import scrolledtext

from tkinter import filedialog as fd

import pyautogui as pag

import itertools

import re as regex

import time

import random as rd

import simpleaudio as sa

import os







# DATA SECTION

from typing import List

alphabet = tuple(_.upper() for _ in "abcdefghijklmnopqrstuvwxyz.,!?") # a tuple of english alphabet and 4 symbols, len = 30

desktop_width, desktop_height = pag.size() # here gets a size of users desktop screen in pixels



# FUNCTIONS SECTION

def decrypting_file():

    """This function, loads a content of a txt file
    into a text_window and call -show_secret- function
    that will translate the encrypted message"""

    global secret_original
    global secret_shown
    text_window["state"] = "normal" # set to normal before the doe below
    secret_original = "" # set to default, or it will load saved previous translation from -secret_original-
    secret_shown = False # set to default, or it won't let the -show_secret- func to run again if user uses decryption button right again after first



    path_ = fd.askopenfilename(title = "Only select files that were encoded using ENIGMA!",
    filetypes = [("Text Files", "*.txt")]) # poke the user to only decrypt files encrypted by ENIGMA previously



    if path_: # if a path provided by filedialog
        with open(path_, "r") as file:
            content = "".join(file.readlines())
        text_window.delete(0.0, tk.END)
        text_window.insert(tk.END, content) # insert the content
        text_window.update() # redraw the window
        time.sleep(1) # wait for a second for drama
        show_secret() # then call this func, it will get the loaded content from text_window and decrypt it
    else:
        ...
        # if a path was not provided, do nothing

def subs_allowed() -> None:

    """This func checks if the digits-dot layout is loaded,
    if so, disables input into substitutions entry,
    because it makes a mess if used with this layout

    Will be called down at the ending of the script,
    to check its check right at the start of the app
    """

    if all([x.get()[:-1].isdigit() and x.get()[-1] == "." for x in entries]):
        substitutions["state"] = "disabled"

def translation() -> str.maketrans: # TODO: comment up

    """Simply returns
    a translation table.
    """
    try:

        return str.maketrans("".join([x.get() for x in entries]), "".join(alphabet))

    except ValueError:
        mb.showinfo(title = "Not full", message = "Please enter substitutions for every letter!\nThey have to be only one symbol long for alphabet layouts!")

def translation_digits_case():

    global secret_shown
    global secret_original

    forward = {k: v for k, v in zip(alphabet, [x.get() for x in entries])} # {"A":"47."} case aka a real letter and an encoding
    # the forward above is takes values from -alphabet- and zip them with gotten values from entries
    backward = {v: k for k, v in forward.items()} # {"47.":"A"} case aka an encoding and a real letter, it is just reversed -forward-
    layout = [x.get() for x in entries] # get all the values from the entries
    initial = text_window.get(0.0, tk.END) # gets initial message that was printed by user into te text_window
    sep = r"[ .]" # a match for regular expression's split method, matches an empty space or a dot

    message = [regex.split(sep, x) for x in text_window.get(0.0, tk.END).splitlines(keepends=1)]
    # split by a dot or an empty space the lines from text_window, keepends means that their new line spec char will be saved
    message = list(itertools.chain(*message)) # flatten nested lists using chain
    message = [x if x else " " for x in message] # trying to find all "" <- not real empty spaces and make them actual empty spaces
    message = [x + "." if x not in ["\n", " "] else x for x in message] # getting the dot, cut of by regex.split, to the keys, if the key is not a new line char or a space, if it is, it goes as it is
    message = [backward[x] if x not in ["\n", " "] and x in layout else x for x in message] # finally, gathering the actual message, calling the ciphering chars from the dict
    # for example is the dict is next {"a":"12", "m":"33"}, as message entered as mama will get 33.12.33.12, and vice versa
    message = ''.join(message) # gather it as a string
    message = message

    if not secret_shown: # if secret was not shown yet, so let's do it
        text_window.delete(0.0, tk.END) # clear the text_window
        text_window.insert(0.0, message) # and insert the message, and show it, if there was 33.12.33.12, it will show that it was the word - mama
        text_window["state"] = "disabled" # disable the text_window, to avoid user's sudden input and mess-ups
        secret_shown = True# reverse, the secret was shown
        secret_original = initial.strip("\n") # save the encoded message that was previously in the text_window, like 33.12.33.12 will be saved, to get it back when we need it. Also strip the string of any new line chars
    else: # if the secret was shown
        text_window["state"] = "normal" # get back the input ability
        text_window.delete(0.0, tk.END) # clear the window
        text_window.insert(0.0, secret_original) # input our initial message aka 33.12.33.12
        secret_shown = False # reverse it, the secret is not visible anymore

def show_secret() -> None:

    """
    Takes a value from -text_window- aka Scrolled text widget
    and translates it via given translation table
    """
    global secret_shown
    global secret_original


    try:
        if all([i.get()[:-1].isdigit() and i.get()[-1] == "." for i in entries]): # in case if all the values from entries are digits with a dot at the end (RANDOM DIGITS), it will go down here
            translation_digits_case()
            return
        else:
            ...


        if not secret_shown: # if False, that means that the real meaning of the encoded text from the text_window was not shown, so goes down to do it

            secret = [x for x in text_window.get(0.0, tk.END)] # get all the input from the text_window aka ScrolledText widget

            original = ''.join(secret).splitlines() # get one single string for convenient translation

            original = [f"{x}\n" for x in original[:-1]] + original[-1:] # save the original encrypted text, to show it back in the text_window, make only the last value to have no new line char at the end
            # Why do we cut off the last element of the original, from having \n char, using this way?
            # Because if we cut off it using something like that as ->
            # -> [f"{x}\n" if x != original[-1] else x for x in original] it may turn out, that two similar valuer will be deleted,
            # but we need, just, the last value to have no new line special char, so we will do it like adding the last value back to the list
            # in which all values got their new line special char


            secret = ''.join(secret).splitlines() # gather all values from text_window.get(), split them by lines
            secret = [f"{x.translate(translation())}\n" for x in secret] # translate them and then add the new line char at the end
            secret = "".join(secret) # join everything into a string

            text_window.delete(0.0, tk.END) # clear out the text_window off the original text
            text_window.insert(0.0, secret)


            secret_shown = True # turn this flag True
            secret_original = original # save the original text into this out global scope variable

            text_window["state"] = "disabled" # prevent user from entering something, during the flash of the secret

        else: # if the secret_shown == False

            text_window["state"] = "normal" # get it back, after the secret was flashed
            text_window.delete(0.0, tk.END) # delete everything from the text_window

            x = "".join(secret_original) # join the secret_original into a string
            text_window.insert(tk.END, x) # and fill the text_window by the original message, if it is

            secret_shown = False # and turn it False

    except TypeError:
        ...

def save_file() -> None:

    """
    Saves the printed text from
    ScrolledText widget assigned
    to TextWindow variable, as a
    txt file.

    :return:None
    """

    path_ = fd.askdirectory()
    if path_: # Here we check if path_ is True, in a case if user does not pick a directory
        path_ = f"{path_}\\SecretScript - {time.time()}.txt" # Creates a file in the returned directory by askdirectory
        with open(path_, "w") as file:

            file.write(text_window.get(0.0, tk.END)) # writes all the content of the ScrolledText widget into a file
            mb.showinfo(title = "Saving....", message = "The file has been saved") # and shows this message

def load_layout() -> None: # Comment this func

    path_ = os.path.join(os.getenv("ALLUSERSPROFILE"), "ENC_DC.txt") # joined path, to save the layout at Windows's 7 ProgramData directory

    try:

        with open(path_, "r") as file: # opens the file ENC_DC.txt

            layout = [x[:-1] for x in file.readlines()] # Extracts items and cuts off all \n aka newLine special char

            layout = [f"{x}." for x in layout[1:] if "ND" in layout] or [chr(int(x)) for x in layout[1:] if "AC" in layout] or [str(x) for x in layout] # then checks ->

            # -> if the values are marked as ND aka NumberDot case, if True, extracts them
            # -> if the values are marked as AC aka Alphabet case, if True, extracts them
            # -> if the previous two == False, just extracts the values from -layout- variable and reassigns

            it = iter(layout) # makes an iterator of -layout- list

            for x in entries: # and by a for loop for tkinter.Entries that are in a list named entries
                x.delete(0, tk.END) # clears out every entry
                x.insert(0, next(it)) # and inserts a value into it

    except FileNotFoundError: # If file does not exist

        ... # Do nothing. Layout cells aka tkinter.Entry widgets won't be filled by values

def save_layout() -> None:

    """
    Function saves the layout

    In case of the layout consists of
    ASCII English letters, it marks
    the beginning of the file, into
    which the layout is saved as AC

    In case of the layout consists of
    digits ending by dots, it marks
    the beginning of the file, into
    which the layout is saved as ND
    NUMBER-DOT case

    All other cases saved with no
    marks at the head of the file,
    right as they are

    I save the letters from the layout,
    converting them by ORD method, just as
    an attempt to make the user's layout
    more protected.

    :return:None
    """

    # this is the similar check as in -clear_textfield- function, starts here
    if ask_before_var.get():
        if mb.askyesno(title="Save..", message=f"{' '*8}Save layout?"):
            ...
        else:
            return
    # ends here, and the main body below

    path_ = os.path.join(os.getenv("ALLUSERSPROFILE"), "ENC_DC.txt") # Joined path into which it saves the layout, ends in ProgramData folder of Windows 7

    if all([bool(x.get()) for x in entries]): # This function would be executed only if all entry.get() funcs of tkinter.Entry widgets return True, and it is True is the string is not empty space

        if len([x.get() for x in entries if x.get() in alphabet]) == 30: # Checks if all results from tkinter.Entry widgets get() method are in the alphabet tuple up there, and if True, goes down

            with open(path_, "w") as file: # Creates a file and marks it by an AC - alphabet case mark
                file.write("AC\n")

            for x in [v.get() for v in entries]: # Saves all results from tkinter.Entry get() method, into a file
                with open(path_, "a") as file: # Here we can use -a- append mode for the writing, because the file already had been created ap at the marking process
                    file.write(f"{ord(x)}\n") # every letter of the layout would be converted into an ASCII number using ORD builtin method of Python

            mb.showinfo(title = "Alphabet layout", message = "Layout has been saved!") # and a message to be shown at the ending of the process

        elif all([x.get()[:-1].isdigit() for x in entries] + [x.get()[-1] == "." for x in entries]): # If the previous checking == False, checks ->

            # -> if the values from tkinter.Entry.get() are digits with a dot at the end, if so, goes down
            # -> a layout that consists of digits with dots at the end is generated when you press -RANDOM-DIGITS- button of the UI

            with open(path_, "w") as file:  # The same marking process as above
                file.write("ND\n") # The beginning of txt file, would be marked as ND, the number-dot case

            for x in [v.get() for v in entries]:
                with open(path_, "a") as file: # Use -a- append mode, because the file had been created
                    file.write(f"{x[:-1]}\n") # write the numbers from tkinter.Entry.get() method, into the file, cutting off the dot by x[:-1] indexing

            mb.showinfo(title="Number-dot layout", message="Layout has been saved!") # shows a message

        else: # In any other cases, layout will be saved as it is

            with open(path_, "w") as file:

                for x in [v.get() for v in entries]:

                    file.write(f"{x}\n")

            mb.showinfo(title="Custom layout", message="Layout has been saved!")

    else: # If all tkinter.Entry do not return something with their get() methods, this whole function would end down here ->

        mb.showinfo(title = "Bad layout", message = "The layout is incomplete! Fill out all entries!") # -> popping put this message box notification

def insert_substitutions(event): #


    """This function inserts random
    predefined chars as an empty space
    substitutions into a textfield!

    Also, it calls -erase_space_enter_sound-
    clicking sounds making function, at the
    beginning.

    I called -erase_space_enter_sound- function
    trough here, because if you do it trough
    dispatcher function and feed the event
    to both the above-mentioned and -insert_substitutions-
    function, the event goes wrong, and I was not able
    to prevent actual empty-space ascii char from
    being inserted into the textfield using

    <if event.keysym:
        return "break">

    trick
    """

    erase_space_enter_sound(event)

    if substitutions.get() and substitutions.get() != "Enter your unique substitutions for Space button": # if there is something in -substitutions- tkinter entry, and it is not equal to the placeholder
        space_subs = set([_ for _ in substitutions.get()]) # then we go down here, and gather everything from the entry into a set, to avoid repeats
        space_subs = list(space_subs) # then convert it back into a list, that is to be used ahead
        space_subs = [x for x in space_subs if x not in [v.get() for v in entries]+[i for i in "1234567890"]] # Symbols that are in the layout and digits won't be accepted as subs

        if event.keysym:
            text_window.insert(tk.INSERT, rd.choice(space_subs))  # here we randomly insert chars from space_subs into text_window, everytime when Space button pressed
            return "break" # return break to prevent actual ascii empty_space char from being inserted

def placeholder_check(event):

    """This function inserts prompt
    string into a tkinter entry
    named -substitutions-"""

    if str(event.type) == "FocusIn" and substitutions.get() == "Enter your unique substitutions for Space button": # Converts event.object into a string and checks, if it is FocusIn == True
        substitutions["state"] = "normal"
        substitutions.delete(0, tk.END) # Then the placeholder text will be deleted
    if str(event.type) == "FocusOut":
        if substitutions.get():
            ...
        else:
            substitutions.insert(0, "Enter your unique substitutions for Space button")

def alphabet_layout():

    """Sets english alphabet chars one to one
    into corresponding entries"""

    global secret_original

    # this is the similar check as in -clear_textfield- function, starts here
    if ask_before_var.get():
        if mb.askyesno(title="ONE TO ONE LAYOUT", message = "Set ordered layout?"):
            ...
        else:
            return
    # ends here, and the main body below

    them = iter(alphabet) # iterates Alphabet tuple
    for _ in entries: # then sets all them into entries
        _.delete(0, tk.END)
        _.insert(0, next(them))
        secret_original = ""  # also clear the saved message
        text_window.delete(0.0, tk.END)  # and clear the textbox
        substitutions["state"] = "normal" # get subs enabled with this layout

def clear_textfield() -> None:

    """Simply clears textfield"""

    global secret_original

    if ask_before_var.get(): # If the checkbox -ask_before_action_checkbutton- active
        if mb.askyesno(title="Clearing", message="Are you sure you want to clear the textfield?"): # ask before action
            ... # and if Yes, it will be skipped down (Where?)
        else:
            return # if No, the function will be ended

    text_window["state"] = "normal" # set it back in case it is disabled
    text_window.delete(0.0, tk.END) # (Here!)
    secret_original = "" # also clear the saved message

def erase_space_enter_sound(event) -> None:

    """This func will be bind,
    and called when Backspace
    or Space button is pushed

    Do not delete -event- argument,
    it is an entry for event.
    """
    if sounds_off_on.get():
        sound = sa.WaveObject.from_wave_file("stroke_1.wav") # here have to be absolute path to the sound, or it won't play it after compilation via auto-py-to-exe, like this C:\Users\SSD\Desktop\New Folder\stroke_1.wav
        sound.play()

def clicking_sound() -> None:

    """simple function to play a sound.
    Will be called by -letter_caller- function"""

    sound = sa.WaveObject.from_wave_file("stroke_2.wav") # here have to be absolute path to the sound, or it won't play it after compilation via auto-py-to-exe, like this C:\Users\SSD\Desktop\New Folder\stroke_1.wav
    return sound.play()

def shuffled_letters_layout() -> None:

    """Does almost the same thing as "random_numbers" function"""

    global secret_original

    if ask_before_var.get(): # this hat, behaves itself similarly as in "random_numbers_layout" function, from here
        if mb.askyesno(title="Generate layout", message="You want to generate layout of random letters?\nOld layout will be erased!"):
            ...
        else:
            return # to here

    alphabet_ = list(alphabet[:26]) # cut off a list of 26 english letters, leaving 4 symbols behind
    rd.shuffle(alphabet_) # shuffle them
    alphabet_ = iter(alphabet_) # make an iterator

    symbols = list(alphabet[26:]) # take the left behind symbols into a separate list
    rd.shuffle(symbols) # shuffle them
    symbols = iter(symbols) # make an iterator

    for _ in entries[:26]: # for tkinter entries which are for letters, ends at 26, because it is the amount of english letters and their corresponding tkinter entries
        _.delete(0, tk.END) # clear up every entry
        _.insert(0, next(alphabet_)) # insert a random letter

    for _ in entries[26:]: # do the same for four symbol entries, starting from 26, where it stopped above
        _.delete(0, tk.END)
        _.insert(0, next(symbols))

    secret_original = ""  # also clear the saved message
    text_window.delete(0.0, tk.END)  # and clear the textbox
    substitutions["state"] = "normal"  # get subs enabled with this layout

def random_numbers_layout(target: List[tk.Entry]) -> None: # the entries list will be an argument for it

    """And this function fill all entries by
    randomly chosen numbers in the given range"""

    global secret_original

    if ask_before_var.get(): # if the checkbox is True, go down and ask yes-no, but if the result is False, go down to the code right away at rd_ = rd
        if mb.askyesno(title="Generate layout", message="You want to generate layout of random numbers?\nOld layout will be erased!"): # if here it gets True, it goes down to the code at rd_ = rd
            ...
        else:
            return # if yes-no, gets No, will return and the func execution will be ended

    rd_ = rd
    layout = set(rd_.randrange(1, 100) for _ in range(200)) # trying to make it more random
    layout = list(layout)
    for _ in range(rd_.randint(1, 7)): # random shuffles to make it even more random
        rd_.shuffle(layout) # shuffle it here
    layout = iter(layout) # iterator
    for _ in target: # put it into each tkinter entry representing alphabet letters
        _.delete(0, tk.END)
        _.insert(0, f"{next(layout)}.")

    secret_original = ""  # also clear the saved message
    text_window.delete(0.0, tk.END)  # and clear the textbox
    substitutions["state"] = "disabled"  # get subs disabled with this layout

def locker() -> None:
    """Conveniently turns all entries into readonly/normal states"""
    for _ in entries:
        if _.cget("state") == "normal":
            _["state"] = "readonly"
        else:
            _["state"] = "normal"

def delete_layout() -> None:

    """

    And this func clears out all entries
    and also deletes the layout file ENC_DC.txt
    from the memory

    The file is saved at ProgramData of Windows 7

    """

    global secret_original
    path_ = os.path.join(os.getenv("ALLUSERSPROFILE"), "ENC_DC.txt")

    if ask_before_var.get(): # This asking procedure works the same as in -random_numbers_layout-, from here
        if mb.askyesno(title = "Deleting layout", message = "Are you sure that you want to delete your layout?\nMake sure you have saved it in a notebook!"):
            ...
        else:
            return # to here

    for i_ in entries: # clears out all tkinter entries from the list named Entries
        i_["state"] = "normal"
        i_.delete(0, "end")

        secret_original = ""  # also clear the saved message
        text_window.delete(0.0, tk.END) # and clear the textbox

    try:
        os.remove(path_)

    except FileNotFoundError: # if the layout file does not exist, catch an Exception
        ...

def letter_caller(bind_event):

    """Every called letter will be bind and inserted
    into the text field by this function"""

    if bind_event.keysym: # if there is a letter in keysym option that holds chars
        if sounds_off_on.get() == True: # if this IntVar is True, sound of clicking type machine is to play at every button stroke
            clicking_sound()
        position = alphabet.index(bind_event.char.upper()) # finds the index of this letter in alphabet tuple above, p.s bind_event.char also have pressed letter as a value
        text_window.insert(tk.INSERT, entries[position].get()) # using -position- value as an index, seeks a letter inserted into a tkinter entry, and inserts it into text window
        return "break" # here we return -break- to prevent actual letter from being inserted into the textfield aka typing window

def binder(x, func_) -> None:

    """Values gotten from the x, will be bind,
    in both lower and uppercase cases. English
    alphabet letters are the values from the x,
    that are to eb bind, using >letter_caller< function"""

    for _ in x:
        text_window.bind(f"<KeyPress-{_}>", func_)
        text_window.bind(f"<KeyPress-{_.lower()}>", func_)

def call_help():

    global help_called

    text_ = """
    This app is just for fun,
    it is not a serious encrypting machine,
    so do not trust it your serious life-depending
    messages, if you are not sure.
    
    How to use:
    
    Enter your substitutes for every letter
    of the English alphabet ✔
    
    Press SAVE LAYOUT button to save
    your entered layout, and start
    printing ✔
    
    After this, you can start printing
    into a text-window above, during which
    every letter pressed by you will be
    substituted by the symbol you provided
    
    Use LOCK\\UNLOCK button to prevent 
    entries of accidental inputs 
    
    For example, if you chose X for D,
    and P for A, word -> dad, will be -> XPX
    
    After you entered a message, use CODE\\ENCODE
    button to switch between encoded message and 
    the message 
    
    RANDOM DIGITS button will provide you by a 
    layout of random digits with a dot at the end
    as a separator 
    
    SAVE FILE button saves any content of the
    textfield as a txt file, at chosen directory 
    
    DELETE LAYOUT deletes substitutions from the 
    entries of the alphabet 
    
    DECRYPT FILE is for decryption of any txt file
    messages encrypted by this same application, 
    choose a file, its content will be loaded into
    the textfield and decoded using provided layout 
    
    SHUFFLED_AL that means shuffled alphabet layout
    will provide you by a layout of randomly set 
    letters of the alphabet 
    
    AS IT IS button will set all letter one to one 
    A is A, B is B and ect 
    
    CLEAR TEXTFIELD deletes any input from 
    the textfield 
    
    HELP button provides this window with this
    message of instructions 
    
    SILENT//CLICKING is used to turn off/turn on
    clicking sound when you print something 
    
    ASK BEFORE ACTION is used to ask you YES/NO
    before you delete a layout, or generate a new
    one, or clear the text window 
    
    Space button substitutions work only with
    one sign to one sign layouts, for example
    it won't work if A is assigned to BXC, to a 
    plural signs, or similarly A is 544, it works
    if for example one sign A is assigned to another
    one sign % or ^ or X or 4.
    
    What space button substitutions do? If you press
    Space button, they will insert a sub instead of 
    empty space, to make your secret message encryption
    more complicated to decrypt. 
    """


    def reset():
        global help_called
        help_called = False
        hw.destroy()

    if not help_called:
        hw = tk.Toplevel() # hw for help window
        hw.geometry("600x600")
        hw.title("Help")

        text = tk.Text(hw, wrap = tk.WORD)
        text.pack(fill = tk.BOTH, expand = 1)

        scroll = tk.Scrollbar(text)
        scroll.config(command = text.yview())
        text.config(yscrollcommand = scroll.set)
        scroll.pack(side = tk.RIGHT, fill = tk.Y)

        text.insert(tk.INSERT, text_)
        text.config(state = "disabled")


        logo_label = tk.Label(hw, text = "FreeWind Interactive © 2024", font = ("Times New Roman", 7))
        logo_label.pack()

        help_called = True
        hw.protocol("WM_DELETE_WINDOW", reset)
    else:
        ...




# ROOT/WINDOWS SECTION
root = tk.Tk()
root.geometry(f"1200x680+{(desktop_width - 1200)//2}+{(desktop_height - 620)//2}") # sets geometry, and position the appearance of the app's window
# Gotten width of the users desktop is 1920 - 1200(the width of the main window) = 720//2 = 360, so the window will be drawn in th middle of the screen, the same for height
root.title("ENIGMA") # and a title
root.resizable(0, 0) # forbid to be resizable


# FLAGS SECTION

secret_shown = False
secret_original = []
help_called = False





# FRAMES SECTION
text_windows_frame = tk.PanedWindow(root)
text_windows_frame.pack(fill = "x", expand = True)

upper_frame = tk.Frame(root)
upper_frame.pack(anchor = "w")

alphabet_frame = tk.Frame(root) # this frame contains all alphabet entries
alphabet_frame.pack()

lower_frame = tk.Frame(root, bd = 5)
lower_frame.pack()

# SCROLLED TEXT SECTION
text_window = tk.scrolledtext.ScrolledText(text_windows_frame, height=15)
text_window.pack(fill = "x", expand = True)

# CHECKBUTTONS SECTION
sounds_off_on = tk.IntVar()
sounds_off_on.set(1)
sounds_off_checkbutton = tk.Checkbutton(upper_frame, text = "SILENT/CLICKING", onvalue = 1, offvalue = 0, variable = sounds_off_on)
sounds_off_checkbutton.grid(row = 0, column = 0)

ask_before_var = tk.IntVar()
ask_before_var.set(1)
ask_before_action_checkbutton = tk.Checkbutton(upper_frame, text = "ASK BEFORE ACTION", onvalue = 1, offvalue = 0, variable = ask_before_var)
ask_before_action_checkbutton.grid(row = 0, column = 1)


# LABELS SECTION
alphabet_labels = [] # the defined labels below will be added into this list for overall actions

for _ in alphabet[:13]: # declaring labels for letters from 0 to 13, to make two rows of letters and entries next to each other

    column_ = alphabet[:13].index(_) # here saves the letter's index to be the column option's value, because _ will be declared as a label, and the index will be lost

    _ = tk.Label(alphabet_frame, text = _) # declares a label into _
    _.grid(row = 0, column = column_) # grids it, using index value as a position for column option
    alphabet_labels.append(_) # append newly created label widget into the list above, for convenient for loop actions

for _ in alphabet[13:26]: # the same as the above will be done here, but for second equal row of letter, starting from 13 to 26

    column_ = alphabet[13:26].index(_)

    _ = tk.Label(alphabet_frame, text = _)
    _.grid(row = 2, column = column_) # here we skip row = 1, because entries have to be placed below the labels
    alphabet_labels.append(_)

for _ in alphabet[26:]: # declares last 4 symbols from the alphabet tuple as labels

    column_ = alphabet[26:].index(_) + 5 # add +5 to make the symbols labels placed in the middle

    _ = tk.Label(alphabet_frame, text = _)
    _.grid(row = 4, column = column_)
    alphabet_labels.append(_)

for i in alphabet_labels: # configuring all the alphabet labels
    i.config(font = ("Times New Roman", 20)) # set a font

logo_label = tk.Label(root, text = "FreeWind Interactive © 2024", font = ("Times New Roman", 7))
logo_label.pack()

# ENTRIES SECTION
entries = [] # the defined entries below will be added into this list for overall actions

# almost similar operations will be made here, as for the labels above

for _ in alphabet[:13]: # entries for each letter and 4 symbols will be declared

    column_ = alphabet[:13].index(_)

    _ = tk.Entry(alphabet_frame)
    _.grid(row = 1, column = column_) # take a note, here, the skipped rows, during the labels' declaration, will be occupied
    entries.append(_)

for _ in alphabet[13:26]: # the same here, as for the entries above

    column_ = alphabet[13:26].index(_)

    _ = tk.Entry(alphabet_frame)
    _.grid(row = 3, column = column_) # again, skipped row at the label's declaration is occupied
    entries.append(_)

for _ in alphabet[26:]: # the same as above, for 4 symbol sings

    column_ = alphabet[26:].index(_) + 5

    _ = tk.Entry(alphabet_frame)
    _.grid(row = 5, column = column_)
    entries.append(_) # also, at each for loop, entry widgets are gathered into a list above

for _ in entries: # here we do configurations for widgets in the list

    _.config(width = 11) # width of the entries is set

load_layout() # Load the layout right after the definition of entries

# Last occupied column by entries made via for loop is 8 and row is 5
substitutions = tk.Entry(alphabet_frame)
substitutions.insert(0, "Enter your unique substitutions for Space button")
substitutions["state"] = "readonly"
substitutions.bind("<FocusIn>", placeholder_check)
substitutions.bind("<FocusOut>", placeholder_check)
substitutions.grid(row = 6, column = 5, pady = 4, columnspan = 4, sticky = "we")


# BUTTONS SECTION

buttons: List[tk.Button] = []

lock_button = tk.Button(lower_frame, text = "UN/LOCK", command = locker)
lock_button.grid(row = 0, column = 0, sticky = "we")

del_layout_button = tk.Button(lower_frame, text = "DELETE LAYOUT", command = delete_layout)
del_layout_button.grid(row = 0, column = 1, sticky = "we")

save_file_button = tk.Button(lower_frame, text ="SAVE FILE", command = save_file)
save_file_button.grid(row = 0, column = 2, sticky ="we")

decrypt_file_button = tk.Button(lower_frame, text ="DECRYPT FILE", command = decrypting_file)
decrypt_file_button.grid(row = 0, column = 3, sticky ="we")

save_layout_button = tk.Button(lower_frame, text ="SAVE LAYOUT", command = save_layout)
save_layout_button.grid(row = 0, column = 4, sticky = "we")

hep = tk.Button(lower_frame, text = "HELP", command = call_help)
hep.grid(row = 0, column = 5, rowspan = 2, sticky = "ns")

random_digits_button = tk.Button(lower_frame, text = "RANDOM DIGITS", command = lambda: random_numbers_layout(entries))
random_digits_button.grid(row = 1, column = 0)

shuffled_letters_button = tk.Button(lower_frame, text = "SHUFFLED AL-LAYOUT", command = shuffled_letters_layout)
shuffled_letters_button.grid(row = 1, column = 1)

alphabet_layout_button = tk.Button(lower_frame, text = "AS IT IS LAYOUT", command = alphabet_layout)
alphabet_layout_button.grid(row = 1, column = 2)

clear_textfield_button = tk.Button(lower_frame, text = "CLEAR TEXTFIELD", command = clear_textfield)
clear_textfield_button.grid(row = 1, column = 3)

test = tk.Button(lower_frame, text ="CODE/ENCODE", command = show_secret)
test.grid(row = 1, column = 4)

for i in globals().values():
    if type(i) is tk.Button:
        buttons.append(i)

for i in buttons:
    i.grid(padx = 2)
    i.grid(pady = 2)

binder(alphabet, letter_caller)
text_window.bind("<space>", insert_substitutions) # binding Space and BackSpace buttons
text_window.bind("<BackSpace>", erase_space_enter_sound) # to make them make clicking sounds too
text_window.bind("<Return>", erase_space_enter_sound)

subs_allowed()

root.mainloop()
