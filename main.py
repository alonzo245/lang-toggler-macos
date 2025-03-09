import time
import threading
import sys
import curses
import os
from pynput import keyboard
from AppKit import NSPasteboard, NSStringPboardType, NSScreen
from Quartz import CGEventCreateKeyboardEvent, CGEventPost, kCGHIDEventTap
import subprocess

def get_screen_size():
    """Get the main screen's width and height."""
    screen = NSScreen.mainScreen().frame()
    screen_width = int(screen.size.width)
    screen_height = int(screen.size.height)
    return screen_width, screen_height

def resize_terminal():
    """Resize, move, and set font size for Terminal or iTerm2."""
    screen_width, screen_height = get_screen_size()
    
    # Define terminal window size
    window_width = 1000  # Adjust width as needed
    window_height = 200  # Adjust height as needed

    # Calculate center position
    x_pos = (screen_width - window_width) // 2  # Center horizontally
    y_pos = screen_height - window_height  # Position at the bottom

    # Get the current active application
    active_app = subprocess.run(
        ["osascript", "-e", 'tell application "System Events" to get name of first process whose frontmost is true'], 
        capture_output=True, text=True
    ).stdout.strip()

    if "iTerm2" in active_app:
        print("[INFO] Resizing iTerm2 window and setting font size...")
        applescript = f"""
        tell application "iTerm2"
            tell current session of current window
                set font size to 40
            end tell
            tell current window
                set bounds to {{{x_pos}, {y_pos}, {x_pos + window_width}, {y_pos + window_height}}}
            end tell
        end tell
        """
    elif "Terminal" in active_app:
        print("[INFO] Resizing Terminal window and setting font size...")
        applescript = f"""
        tell application "Terminal"
            set bounds of front window to {{{x_pos}, {y_pos}, {x_pos + window_width}, {y_pos + window_height}}}
            tell front window
                set font size of front tab to 40
            end tell
        end tell
        """
    else:
        print("[WARNING] No recognized terminal detected. Skipping resize.")
        return
    
    os.system(f"osascript -e '{applescript}'")

# Call function to resize terminal and set font size when script starts
resize_terminal()

# English to Hebrew Keyboard Mapping
EN_TO_HE_HEBREW = {
    'a': 'ש', 'b': 'נ', 'c': 'ב', 'd': 'ג', 'e': 'ק', 'f': 'כ', 'g': 'ע', 'h': 'י', 'i': 'ן', 'j': 'ח',
    'k': 'ל', 'l': 'ך', 'm': 'צ', 'n': 'מ', 'o': 'ם', 'p': 'פ', 'q': '/', 'r': 'ר', 's': 'ד', 't': 'א',
    'u': 'ו', 'v': 'ה', 'w': "'", 'x': 'ס', 'y': 'ט', 'z': 'ז', ';': 'ף', ',': 'ת', '.': 'ץ', '/': '.',
    "'": ',', '[': ']', ']': '[', '\\': '\\'
}

# Hebrew to English Keyboard Mapping (Reverse)
HE_TO_EN_HEBREW = {v: k for k, v in EN_TO_HE_HEBREW.items()}

def detect_language(text):
    """Detect whether text is mostly Hebrew or English based on character distribution."""
    hebrew_chars = sum(1 for char in text if 'א' <= char <= 'ת')
    english_chars = sum(1 for char in text if 'a' <= char <= 'z' or 'A' <= char <= 'Z')
    
    return 'hebrew' if hebrew_chars > english_chars else 'english'

def convert_text(text):
    """Convert text between Hebrew and English based on detected language."""
    lang = detect_language(text)
    
    if lang == 'hebrew':
        return ''.join(HE_TO_EN_HEBREW.get(char, char) for char in text)
    else:
        return ''.join(EN_TO_HE_HEBREW.get(char, char) for char in text)

def get_clipboard_text():
    """Retrieve text from the clipboard."""
    pb = NSPasteboard.generalPasteboard()
    content = pb.stringForType_(NSStringPboardType)
    return str(content) if content else ""

def set_clipboard_text(text):
    """Set text to clipboard."""
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()
    pb.setString_forType_(text, NSStringPboardType)

def simulate_paste():
    """Simulate Command + V to paste the converted text."""
    event_down = CGEventCreateKeyboardEvent(None, 9, True)  # 9 is "V"
    event_up = CGEventCreateKeyboardEvent(None, 9, False)
    CGEventPost(kCGHIDEventTap, event_down)
    CGEventPost(kCGHIDEventTap, event_up)

def select_entire_line():
    """Simulate keyboard shortcuts to select the entire line."""
    kb = keyboard.Controller()
    
    # Move cursor to the beginning of the line (Cmd + Left)
    with kb.pressed(keyboard.Key.cmd):
        kb.press(keyboard.Key.left)
        kb.release(keyboard.Key.left)

    time.sleep(0.1)  # Small delay to ensure the command registers

    # Select entire line (Shift + Cmd + Right)
    with kb.pressed(keyboard.Key.shift, keyboard.Key.cmd):
        kb.press(keyboard.Key.right)
        kb.release(keyboard.Key.right)

    time.sleep(0.1)  # Small delay to ensure selection registers

def on_activate():
    """Triggered when Ctrl + S is pressed."""
    print("\n[INFO] Selecting, converting, and pasting text...")

    kb = keyboard.Controller()
    
    # Select entire line
    select_entire_line()

    # Copy selected text
    with kb.pressed(keyboard.Key.cmd):
        kb.press('c')
        kb.release('c')

    time.sleep(0.3)  # Allow time for clipboard update
    selected_text = get_clipboard_text()

    if selected_text:
        converted_text = convert_text(selected_text)
        set_clipboard_text(converted_text)
        
        time.sleep(0.3)  # Ensure clipboard is updated
        
        # Paste converted text
        with kb.pressed(keyboard.Key.cmd):
            kb.press('v')
            kb.release('v')
        
        print(f"[SUCCESS] Text converted and pasted! (Detected: {detect_language(selected_text)})")

# Variable to store logged keystrokes
keystroke_log = ""
last_keystroke_time = time.time()
pressed_keys = set()  # Track pressed keys

def clear_keystrokes():
    """Clear keystroke display after 5 seconds of inactivity."""
    global keystroke_log
    while True:
        time.sleep(1)
        if time.time() - last_keystroke_time >= 3:
            keystroke_log = ""

def on_key_press(key):
    """Track pressed keys and trigger conversion on Ctrl + S."""
    global keystroke_log, last_keystroke_time, pressed_keys

    try:
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            pressed_keys.add(key)
        elif hasattr(key, 'char') and key.char is not None:
            if 's' in key.char and (keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys):
                on_activate()
            else:
                keystroke_log += key.char
                last_keystroke_time = time.time()
    except Exception as e:
        print(f"Error: {e}")

def on_key_release(key):
    """Handle key release and stop the listener on ESC."""
    global pressed_keys
    if key == keyboard.Key.esc:
        print("\nExiting...")
        return False  # Stop listener
    elif key in pressed_keys:
        pressed_keys.remove(key)

def keystroke_window(stdscr):
    """Create a curses window to display keystrokes."""
    global keystroke_log
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    while True:
        stdscr.clear()
        stdscr.addstr(1, 1, "Keystrokes: " + keystroke_log[-50:])
        stdscr.refresh()
        time.sleep(0.1)

# Start the background thread to clear keystrokes after 5s
t = threading.Thread(target=clear_keystrokes, daemon=True)
t.start()

# Start keyboard listener
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    curses.wrapper(keystroke_window)
    listener.join()


