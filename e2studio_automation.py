import sys
import os
import time

# Add submodule paths to sys.path so we can import from them natively
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'pywinauto_src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'clipboard_src')))

from pywinauto.application import Application
from pywinauto.keyboard import send_keys

def log(msg):
    print(msg, file=sys.stderr)

class E2StudioAutomation:
    def __init__(self):
        # 1. Connect to Running e2 studio (Must use UIA for Eclipse/SWT)
        log(">> Hooking into e2 studio...")
        self.app = Application(backend="uia").connect(path="e2studio.exe")
        self.main_win = self.app.window(title_re=".*e2 studio")
        self.main_win.set_focus()

    def open_view(self, category, view_name):
        """Drives the Window -> Show View -> Other menu to open specific debug views."""
        log(f">> Opening view: {category} -> {view_name}")
        self.main_win.menu_select("Window->Show View->Other...")
        time.sleep(0.5)
        # Type to filter, or navigate the tree
        dialog = self.app.ShowView
        # Assuming we can find it via the Tree control in the dialog
        try:
            tree_item_path = f"\\{category}\\{view_name}"
            dialog.tree_view.get_item(tree_item_path).select()
        except Exception:
            # Fallback: type the view name in the filter text box
            dialog.type_keys(view_name)
            time.sleep(0.5)
            dialog.type_keys("{DOWN}{ENTER}")
            return
        dialog.OK.click()
        time.sleep(1)

    def extract_variable_expression(self, var_name):
        # 2. Ensure Expressions View is Open
        log(f">> Extracting variable: {var_name}")
        self.main_win.type_keys("%+q")
        time.sleep(0.5)
        self.main_win.type_keys("x")
        time.sleep(1)

        # 3. Add/Select Variable
        send_keys("{INSERT}")
        send_keys(f"{var_name}{{ENTER}}")
        time.sleep(1)

        # 4. Extract "Ground Truth" (The Value)
        try:
            tree = self.main_win.child_window(control_type="Tree")
            item = tree.get_item(f"\\{var_name}")
            val = item.legacy_iaccessible_value()
            log(f"CAPTURED VALUE (Method A): {val}")
            return val
        except Exception as e:
            log(">> UI Read failed. Attempting Clipboard Fallback...")
            send_keys("^c") # Ctrl+C
            try:
                import clipboard
                val = clipboard.paste()
            except ImportError:
                log(">> Warning: clipboard submodule failed to load.")
                val = "N/A"
            log(f"CAPTURED VALUE (Method B): {val}")
            return val

    # --- Full GDB Mode Features ---
    def open_registers_view(self):
        """Opens the Registers view to inspect CPU state."""
        self.open_view("Debug", "Registers")

    def open_memory_view(self):
        """Opens the Memory view to inspect RAM/Flash."""
        self.open_view("Debug", "Memory")

    def open_debug_view(self):
        """Opens the Debug view to inspect the Call Stack and Threads."""
        self.open_view("Debug", "Debug")

    def open_rtos_resources_view(self):
        """Opens RTOS specific views (e.g., FreeRTOS or ThreadX Queues/Tasks)."""
        # Exact path depends on the installed RTOS plugin, using common naming
        self.open_view("RTOS", "RTOS Resources")

    # --- Debug Execution Controls ---
    def step_into(self):
        """Simulate F5 - Step Into"""
        log(">> Stepping Into (F5)...")
        self.main_win.type_keys("{F5}")

    def step_over(self):
        """Simulate F6 - Step Over"""
        log(">> Stepping Over (F6)...")
        self.main_win.type_keys("{F6}")

    def resume(self):
        """Simulate F8 - Resume Execution"""
        log(">> Resuming Execution (F8)...")
        self.main_win.type_keys("{F8}")

    def suspend(self):
        """Suspend execution. Usually requires finding the Suspend button on the toolbar."""
        log(">> Suspending Execution...")
        # Fallback to menu if direct shortcut doesn't exist
        self.main_win.menu_select("Run->Suspend")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="e2 studio Automation CLI")
    parser.add_argument("action", choices=[
        "extract", "step_into", "step_over", "resume", "suspend",
        "open_registers", "open_memory", "open_debug", "open_rtos"
    ], help="The action to perform")
    parser.add_argument("--var", help="The variable name to extract (required for 'extract' action)")

    args = parser.parse_args()

    e2 = E2StudioAutomation()

    if args.action == "extract":
        if not args.var:
            log("Error: --var is required for extract action")
            sys.exit(1)
        # Ensure only the value is printed to stdout so the extension can capture it easily
        # Everything else is routed to stderr via log()
        print(e2.extract_variable_expression(args.var))
    elif args.action == "step_into":
        e2.step_into()
    elif args.action == "step_over":
        e2.step_over()
    elif args.action == "resume":
        e2.resume()
    elif args.action == "suspend":
        e2.suspend()
    elif args.action == "open_registers":
        e2.open_registers_view()
    elif args.action == "open_memory":
        e2.open_memory_view()
    elif args.action == "open_debug":
        e2.open_debug_view()
    elif args.action == "open_rtos":
        e2.open_rtos_resources_view()
