import sys
import os
import time

# Add submodule paths to sys.path so we can import from them natively
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'pywinauto_src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'clipboard_src')))

from pywinauto.application import Application
from pywinauto.keyboard import send_keys

# 1. Connect to Running e2 studio (Must use UIA for Eclipse/SWT)
print(">> Hooking into e2 studio...")
app = Application(backend="uia").connect(path="e2studio.exe")
main_win = app.window(title_re=".*e2 studio")
main_win.set_focus()

# 2. Ensure Expressions View is Open
# Note: Eclipse menus can be tricky. If menu_select fails, use shortcut:
# Alt+Shift+Q, then X (Standard Eclipse shortcut for Expressions)
main_win.type_keys("%+q")
time.sleep(0.5)
main_win.type_keys("x")

# 3. Add/Select Variable
# We assume the focus is now on the Expressions View.
# We add a variable to ensure it's there.
send_keys("{INSERT}") # Or click 'Add new expression'
send_keys("my_sensor_value{ENTER}")
time.sleep(1)

# 4. Extract "Ground Truth" (The Value)
# Strategy: Eclipse Tables are often 'Tree' controls in UIA.
# We look for the row containing our variable.
try:
    # This finds the tree item in the focused pane
    tree = main_win.child_window(control_type="Tree")

    # Get the item (You may need to adjust the path separator '->')
    # In some Eclipse versions, values are in a separate column (Header)
    item = tree.get_item("\\my_sensor_value")

    # METHOD A: Direct Property Read
    # Eclipse often stores the value in the 'legacy_iaccessible_value' or name
    val = item.legacy_iaccessible_value()
    print(f"CAPTURED VALUE (Method A): {val}")

except Exception as e:
    print(">> UI Read failed. Attempting Clipboard Fallback...")

    # METHOD B: The Clipboard Hack (Universal Fallback)
    # If we can't read the object, we copy it.
    send_keys("^c") # Ctrl+C
    try:
        import clipboard
        val = clipboard.paste()
    except ImportError:
        print(">> Warning: clipboard submodule failed to load.")
        val = "N/A"
    print(f"CAPTURED VALUE (Method B): {val}")
