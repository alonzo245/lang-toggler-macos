Lang-Toggler

Overview

Lang-Toggler is a macOS utility that allows users to seamlessly toggle between Hebrew and English keyboard input. It automatically detects the language of the selected text, converts it, and pastes the translated text back into the active field. The script also resizes and centers the terminal window for an optimized user experience.

Features
	•	Automatic Language Detection: Identifies if the copied text is in Hebrew or English.
	•	Smart Text Conversion: Converts text based on keyboard mappings for accurate toggling.
	•	Clipboard Integration: Copies, processes, and pastes text automatically.
	•	Terminal Resizing: Adjusts and centers the terminal window dynamically.
	•	Keystroke Logging: Tracks key inputs and displays them in a minimal UI.
	•	Hotkey Activation: Press Ctrl + S to trigger the language toggle.
	•	macOS Terminal/iTerm2 Support: Works seamlessly with macOS terminal applications.

Installation

Prerequisites

Ensure you have the following dependencies installed:
	•	Python 3
	•	pynput (for keyboard input tracking)
	•	AppKit and Quartz (for macOS clipboard and event handling)
	•	curses (for UI display)

Install dependencies using:

pip install pynput pyobjc-framework-AppKit pyobjc-framework-Quartz

Usage
	1.	Run the script:

python lang-toggler.py


	2.	Use Ctrl + S to trigger the conversion process:
	•	It selects the entire line.
	•	Copies the text.
	•	Detects the language.
	•	Converts the text.
	•	Pastes the converted text.
	3.	Exit: Press ESC to stop the script.

Key Components
	•	Language Detection: Determines if the input text is Hebrew or English.
	•	Text Conversion: Uses predefined keyboard mappings to switch between Hebrew and English.
	•	Clipboard Management: Uses macOS NSPasteboard for copying and pasting text.
	•	Terminal Resizing: Adjusts window position and font size dynamically.
	•	Keystroke Tracking: Logs keystrokes and provides a simple UI for debugging.

Hotkeys

Shortcut	Function
Ctrl + S	Convert and paste the text
ESC	Exit the script

Known Issues & Limitations
	•	Only works on macOS.
	•	Requires terminal permissions to interact with clipboard and simulate key events.
	•	May not work properly in non-standard applications that restrict key events.

Contribution

Feel free to fork, modify, and improve the script. If you have any feature requests or bug reports, submit an issue on GitHub.

⸻

This README provides a clear overview of your Lang-Toggler project. Let me know if you need modifications! 🚀
