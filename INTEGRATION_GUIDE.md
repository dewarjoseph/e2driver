# Google Antigravity IDE Integration Guide for e² studio Automation

This guide explains how an AI Agent or User can invoke the e² studio automation hooks from within the Google Antigravity IDE (VS Code fork).

## Overview

The `e2studio-automation-0.0.1.vsix` extension registers several "Commands" in the IDE. These commands act as wrappers that spawn our `e2studio_automation.py` script via `child_process`. By triggering these commands, an agent can perform UI-driven debugging inside the Renesas e² studio desktop application without needing internal GDB scripting.

## Installation

1. Drag and drop `e2studio-automation-0.0.1.vsix` into the Google Antigravity IDE Extensions pane, or use the Command Palette -> `Extensions: Install from VSIX...`
2. Ensure you have a workspace folder open containing the `e2studio_automation.py` script and the `pywinauto_src`/`clipboard_src` submodules. (Alternatively, if installed globally, the script resolves its relative paths correctly).
3. Ensure Python 3 is installed and in your system's `PATH`.

## AI Agent Integration (Workflow / Skills)

If you are writing a workflow, skill, or rule for an AI Agent inside the IDE, you can execute these commands programmatically using the standard VS Code Extension API.

### Executing via Code (Agent Skill)

An agent running inside the IDE's extension host can trigger a command like this:

```javascript
// Step Over in the debugger
await vscode.commands.executeCommand('e2studio.stepOver');

// Open the Registers View
await vscode.commands.executeCommand('e2studio.openRegisters');

// Extract a variable
// (Note: The user will be prompted by an Input Box for the variable name,
//  or the command can be adapted to accept string arguments).
await vscode.commands.executeCommand('e2studio.extractVariable');
```

### Registered Commands Reference

| Command ID | Title / Purpose |
|------------|-----------------|
| `e2studio.extractVariable` | Prompts for a variable name, then extracts it from the Expressions view. |
| `e2studio.stepOver` | Simulates pressing `F6` to step over in the e² studio debugger. |
| `e2studio.openRegisters` | Navigates the UI to open the CPU Registers debug view. |

## Customization

Because we use Git Submodules for our external dependencies (`pywinauto`, `clipboard`), the agent can navigate to `pywinauto_src/` or `clipboard_src/` to modify the automation logic at a granular level before executing the VS Code commands.