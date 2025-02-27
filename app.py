'''
Some Poems(remove the poem if it lead to deduction)
I love CSC1002 :)
Though this code is hard.
Which had been burning my head.
I know this is not the best.
But for me, the experience a treasure.
I will remember it forever.

This is a simple Console-Based Editor designed for one-line text editing.
Modules: re
Commands:
    ? - display this help info
    . - toggle row cursor on and off (affects display only)
    h - move cursor left (only if cursor is visible)
    l - move cursor right (only if cursor is visible)
    ^ - move cursor to the beginning of the line (only if cursor is visible)
    $ - move cursor to the end of the line (only if cursor is visible)
    w - move cursor to beginning of next word (only if cursor is visible)
    b - move cursor to beginning of previous word (only if cursor is visible)
    i - insert <text> before cursor (cursor does not change)
    a - append <text> after cursor (cursor does not change)
    x - delete character at cursor (cursor does not change)
    dw - delete word from cursor to beginning of next word (or end of line)
    u - undo previous command
    r - repeat last command
    s - show content
    q - quit program

Note:
    The text editing commands (i, a, x, dw, etc.) work regardless of whether the cursor is shown. The toggle (.) command affects only the visual highlight of the cursor position.
    Only show_content function displays the present content, for other functions, they only change the global variable DISPLAY_TEXT and excute the show_content to show the present content except for the quit function.
'''
import re

#global variables
CURSOR_POSITION = 0
CURSOR_VISIBLE = False
DISPLAY_TEXT = ""
LAST_DISTPLAY_TEXT = ''
LAST_CURSOR_POST = 0
IS_CONTINUE = True
TEXT_HISTORY = []
CMD_HISTORY = []

def display_help():
    help_info = '''? - display this help info
. - toggle row cursor on and off
h - move cursor left 
l - move cursor right 
^ - move cursor to the beginning of the line 
$ - move cursor to the end of the line 
w - move cursor to beginning of next word
b - move cursor to beginning of previous word  
i - insert <text> before cursor 
a - append <text> after cursor 
x - delete character at cursor 
dw - delete word from cursor to beginning of next word (or end of line)
u - undo previous command
r - repeat last command
s - show content
q - quit program'''
    print(help_info)


def show_content():
    '''
    Only change the variable DISPLAY_TEXT
    Only print the content and display cursor if applicable. Do not change the content, or change the position of the cursor.
    '''
    global DISPLAY_TEXT, CURSOR_VISIBLE, CURSOR_POSITION
    # Ensure cursor position is within valid range
    if CURSOR_POSITION >= len(DISPLAY_TEXT):
        CURSOR_POSITION = max(0, len(DISPLAY_TEXT) - 1)
    # Print the cursor
    if CURSOR_VISIBLE and DISPLAY_TEXT and 0 <= CURSOR_POSITION < len(DISPLAY_TEXT):
        print(DISPLAY_TEXT[:CURSOR_POSITION] + "\033[42m" + DISPLAY_TEXT[CURSOR_POSITION] + "\033[0m" + DISPLAY_TEXT[CURSOR_POSITION+1:])
    else:
        print(DISPLAY_TEXT)

def toggle_cursor():
    '''
    Only change the variable CURSOR_VISIBLE
    '''
    global CURSOR_VISIBLE, DISPLAY_TEXT
    # if len(DISPLAY_TEXT) !=0:
    CURSOR_VISIBLE = not CURSOR_VISIBLE
    show_content()

def move_cursor_left():
    '''
    Only change the variable CURSOR_POSITION
    '''
    global CURSOR_POSITION
    if CURSOR_POSITION > 0:
        CURSOR_POSITION -= 1
    show_content()

def move_cursor_right():
    '''
    Only change the variable CURSOR_POSITION
    '''
    global CURSOR_POSITION
    if CURSOR_POSITION < len(DISPLAY_TEXT)-1:
        CURSOR_POSITION += 1
    show_content()

def move_cursor_to_beginning():
    '''
    Only change the variable CURSOR_POSITION
    '''
    global CURSOR_POSITION
    CURSOR_POSITION = 0
    show_content()

def move_cursor_to_end():
    '''
    Only change the variable CURSOR_POSITION
    '''
    global CURSOR_POSITION
    CURSOR_POSITION = len(DISPLAY_TEXT)-1 #index != order
    show_content()

def move_cursor_to_previous_word():
    '''
    Move cursor to the beginning of the current word if cursor is in the middle of a word,
    otherwise move to the beginning of the previous word.
    A word is defined as any sequence of non-whitespace characters.
    '''
    global CURSOR_POSITION
    if CURSOR_POSITION == 0:
        return 
    i = CURSOR_POSITION - 1
    # Skip spaces to find the end of the previous word
    while i > 0 and DISPLAY_TEXT[i].isspace():
        i -= 1
    # Skip the current word to find its beginning
    while i > 0 and not DISPLAY_TEXT[i].isspace():
        i -= 1
    # If we stopped at a space, move one step forward to the start of the word
    if DISPLAY_TEXT[i].isspace() and i < len(DISPLAY_TEXT) - 1:
        i += 1
    CURSOR_POSITION = i
    show_content()

def move_cursor_to_next_word():
    '''
    Only change the variable CURSOR_POSITION
    Move cursor to the beginning of the next word.
    A word is defined as any sequence of non-whitespace characters.
    '''
    global CURSOR_POSITION
    text_after_cursor = DISPLAY_TEXT[CURSOR_POSITION:]
    
    # if the current position is not a space, find the next space
    if not DISPLAY_TEXT[CURSOR_POSITION].isspace():
        # find the first space after the current position
        match = re.search(r'\s', text_after_cursor)
        if match:
            CURSOR_POSITION += match.start()
        else:
            # if there is no space, do not move the cursor
            show_content()
            return
    
    # Find the next non-whitespace character
    match = re.search(r'\S', text_after_cursor[CURSOR_POSITION-len(DISPLAY_TEXT):])
    if match:
        CURSOR_POSITION += match.start()  
    show_content()

def save_state():
    '''
    Save the current state of DISPLAY_TEXT, CURSOR_POSITION, and CURSOR_VISIBLE
    '''
    global DISPLAY_TEXT, CURSOR_POSITION, CURSOR_VISIBLE, TEXT_HISTORY
    TEXT_HISTORY.append((DISPLAY_TEXT[:], CURSOR_POSITION, CURSOR_VISIBLE))

def undo():
    '''
    Revert to the previous state using TEXT_HISTORY
    Support all commands including cursor movements
    Use pop to remove the last state and put it to the current state.
    '''
    global DISPLAY_TEXT, CURSOR_POSITION, CURSOR_VISIBLE, TEXT_HISTORY
    if len(TEXT_HISTORY) > 1:
        TEXT_HISTORY.pop()
        DISPLAY_TEXT, CURSOR_POSITION, CURSOR_VISIBLE = TEXT_HISTORY.pop()
    elif len(TEXT_HISTORY) == 1: # In case there's only one state
        TEXT_HISTORY.pop()
        DISPLAY_TEXT, CURSOR_POSITION, CURSOR_VISIBLE = '', 0, False
    show_content()

def insert_text(text):
    '''
    Insert text at current cursor position
    '''
    global DISPLAY_TEXT, CURSOR_POSITION
    DISPLAY_TEXT = DISPLAY_TEXT[:CURSOR_POSITION] + text + DISPLAY_TEXT[CURSOR_POSITION:]
    CURSOR_POSITION += 0
    show_content()

def append_text(text):
    '''
    Append text after current cursor position
    '''
    global DISPLAY_TEXT, CURSOR_POSITION
    DISPLAY_TEXT = DISPLAY_TEXT[:CURSOR_POSITION + 1] + text + DISPLAY_TEXT[CURSOR_POSITION + 1:]
    CURSOR_POSITION += len(text)
    show_content()

def delete_char():
    '''
    Delete character at cursor position
    '''
    global DISPLAY_TEXT, CURSOR_POSITION
    if CURSOR_POSITION < len(DISPLAY_TEXT):
        DISPLAY_TEXT = DISPLAY_TEXT[:CURSOR_POSITION] + DISPLAY_TEXT[CURSOR_POSITION + 1:]
    show_content()

def delete_word():
    '''
    Delete word at cursor position
    '''
    global DISPLAY_TEXT, CURSOR_POSITION
    if CURSOR_POSITION >= len(DISPLAY_TEXT):
        return

    i = CURSOR_POSITION
    # If starting from space, skip all spaces
    if DISPLAY_TEXT[i].isspace():
        while i < len(DISPLAY_TEXT) and DISPLAY_TEXT[i].isspace():
            i += 1
    else:
        # If starting from non-space, skip until we find space
        while i < len(DISPLAY_TEXT) and not DISPLAY_TEXT[i].isspace():
            i += 1
        # Then skip all spaces
        while i < len(DISPLAY_TEXT) and DISPLAY_TEXT[i].isspace():
            i += 1

    # Delete from cursor to position i
    DISPLAY_TEXT = DISPLAY_TEXT[:CURSOR_POSITION] + DISPLAY_TEXT[i:]
    show_content()

def repeat():
    '''
    Execute the last valid command (excluding u and ?)
    After undo, repeat executes the command before undo
    '''
    global DISPLAY_TEXT, COMMAND_MAP, CMD_HISTORY
    if CMD_HISTORY:
        # find the last valid command
        for cmd, text in reversed(CMD_HISTORY):
            if cmd not in ['u', '?', '$', '^', 's', 'q', 'r']:
                if cmd in COMMAND_MAP:
                    if cmd in ['i', 'a']:
                        COMMAND_MAP[cmd](text)
                    else:
                        COMMAND_MAP[cmd]()
                break
            else:
                continue

def quit_cmd():
    '''
    Only change the variable IS_CONTINUE
    '''
    global IS_CONTINUE
    IS_CONTINUE = False

def parse_command(input_str: str):
    '''
    Parse the input string into a command and optional text.
    Returns a tuple (command, text).
    Use RE to tell the command and text.
    '''
    # Corrected regex pattern (removed slashes/flags)
    pattern = r'^([ia])(.*)$|^(dw|[?\.^$hlwbuxrsq])$'
    # Use fullmatch to ensure entire string is matched
    match = re.fullmatch(pattern, input_str)
    if match:
        if match.group(1):  # i/a command branch
            command = match.group(1)
            text = match.group(2)
        else:  # other commands branch
            command = match.group(3)
            text = ''
    else:
        command, text = '', ''
    
    # print(f"Parsed command: {command!r}, text: {text!r}")
    return command, text

COMMAND_MAP = {
    '?': display_help,
    '.': toggle_cursor,
    'h': move_cursor_left,
    'l': move_cursor_right,
    '^': move_cursor_to_beginning,
    '$': move_cursor_to_end,
    'w': move_cursor_to_next_word,
    'b': move_cursor_to_previous_word,
    'i': insert_text,
    'a': append_text,
    'x': delete_char,
    'dw': delete_word,
    'u': undo,
    'r': repeat,
    's': show_content,
    'q': quit_cmd,
}

if __name__ == '__main__':
    while IS_CONTINUE:
        input_str = input(">")
        cmd, text = parse_command(input_str)
        if cmd in COMMAND_MAP:
            if cmd not in ['?', 'r']:
                CMD_HISTORY.append([cmd, text])
            if cmd in ['i', 'a']:
                COMMAND_MAP[cmd](text)
            else:
                COMMAND_MAP[cmd]()
        else:
            show_content()
        if cmd not in ['?', 'r', 'u']:
            save_state()# In this case, the current state is stored, so pop twice in case of undo and repeat.