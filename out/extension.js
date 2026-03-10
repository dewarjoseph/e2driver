"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const child_process_1 = require("child_process");
const path = require("path");
// Helper to run the Python script via CLI arguments
function runPythonCLI(context, args) {
    return new Promise((resolve, reject) => {
        // Find the absolute path to e2studio_automation.py within the packaged extension directory
        const scriptPath = path.join(context.extensionPath, 'e2studio_automation.py');
        // Using execFile is much safer than exec string interpolation and prevents command injection
        (0, child_process_1.execFile)('python', [scriptPath, ...args], (error, stdout, stderr) => {
            if (error) {
                vscode.window.showErrorMessage(`e2 studio automation failed: ${error.message}`);
                reject(error);
                return;
            }
            if (stderr) {
                console.warn(`e2 studio automation stderr: ${stderr}`);
            }
            // Clean up output to just the value
            const output = stdout.trim();
            vscode.window.showInformationMessage(`Result: ${output}`);
            resolve(output);
        });
    });
}
function activate(context) {
    console.log('Extension "e2studio-automation" is now active.');
    // Command: Extract Variable
    // Accepts an optional argument `varName` allowing programmatic/agent invocation without UI blocking
    let disposableExtract = vscode.commands.registerCommand('e2studio.extractVariable', async (agentVarName) => {
        let varName = agentVarName;
        // If no arg is passed (e.g. invoked manually by a human via Command Palette), show input box
        if (!varName) {
            varName = await vscode.window.showInputBox({
                prompt: 'Enter the variable name to extract from e2 studio',
                placeHolder: 'e.g., my_sensor_value'
            });
        }
        if (varName) {
            vscode.window.showInformationMessage(`Extracting variable: ${varName}`);
            // Pass the arguments safely via execFile array
            return await runPythonCLI(context, ['extract', '--var', varName]);
        }
        return null;
    });
    // --- Execution Controls ---
    let disposableStepInto = vscode.commands.registerCommand('e2studio.stepInto', async () => {
        vscode.window.showInformationMessage('Stepping into in e2 studio...');
        return await runPythonCLI(context, ['step_into']);
    });
    let disposableStepOver = vscode.commands.registerCommand('e2studio.stepOver', async () => {
        vscode.window.showInformationMessage('Stepping over in e2 studio...');
        return await runPythonCLI(context, ['step_over']);
    });
    let disposableResume = vscode.commands.registerCommand('e2studio.resume', async () => {
        vscode.window.showInformationMessage('Resuming execution in e2 studio...');
        return await runPythonCLI(context, ['resume']);
    });
    let disposableSuspend = vscode.commands.registerCommand('e2studio.suspend', async () => {
        vscode.window.showInformationMessage('Suspending execution in e2 studio...');
        return await runPythonCLI(context, ['suspend']);
    });
    // --- Views ---
    let disposableOpenRegisters = vscode.commands.registerCommand('e2studio.openRegisters', async () => {
        vscode.window.showInformationMessage('Opening Registers View in e2 studio...');
        return await runPythonCLI(context, ['open_registers']);
    });
    let disposableOpenMemory = vscode.commands.registerCommand('e2studio.openMemory', async () => {
        vscode.window.showInformationMessage('Opening Memory View in e2 studio...');
        return await runPythonCLI(context, ['open_memory']);
    });
    let disposableOpenDebug = vscode.commands.registerCommand('e2studio.openDebug', async () => {
        vscode.window.showInformationMessage('Opening Debug View in e2 studio...');
        return await runPythonCLI(context, ['open_debug']);
    });
    let disposableOpenRtos = vscode.commands.registerCommand('e2studio.openRtos', async () => {
        vscode.window.showInformationMessage('Opening RTOS Resources View in e2 studio...');
        return await runPythonCLI(context, ['open_rtos']);
    });
    // Register all
    context.subscriptions.push(disposableExtract);
    context.subscriptions.push(disposableStepInto);
    context.subscriptions.push(disposableStepOver);
    context.subscriptions.push(disposableResume);
    context.subscriptions.push(disposableSuspend);
    context.subscriptions.push(disposableOpenRegisters);
    context.subscriptions.push(disposableOpenMemory);
    context.subscriptions.push(disposableOpenDebug);
    context.subscriptions.push(disposableOpenRtos);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map