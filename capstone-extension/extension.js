const vscode = require('vscode');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

function activate(context) {
    console.log("Capstone Extension Active!");

    let disposable1 = vscode.commands.registerCommand('capstone-extension.runSetup', function () {
    const projectPath = path.join(context.globalStorageUri.fsPath, "Automated-Instrumentation-of-Programs");
    console.log(`PROJECT Path (Windows): ${projectPath}`);
    if (!fs.existsSync(projectPath)) {
        vscode.window.showInformationMessage("Cloning Capstone project , please wait...");
        exec(`git clone https://github.com/Basmamohammed123/Automated-Instrumentation-of-Programs.git ${projectPath}`, (err, stdout, stderr) => {
            if (err) {
                vscode.window.showErrorMessage("Failed to clone project: " + stderr);
            } else {
                vscode.window.showInformationMessage("Project cloned successfully!");
                console.log("Project cloned successfully:", stdout);

                const setupScriptPath = path.join(projectPath, "setup-venv.ps1");
                vscode.window.showInformationMessage("Setting up Virtual Environment. This may take a while!" , setupScriptPath);
                
                exec(`cd "${projectPath}" && powershell -ExecutionPolicy Bypass -NoProfile -Command ".\\setup-venv.ps1"`, 
                    (setupErr, setupStdout, setupStderr) => {
                        if (setupErr) {
                            vscode.window.showErrorMessage("Failed to set up virtual environment: " + setupStderr);
                            console.error("Setup script error:", setupStderr);
                        } else {
                            vscode.window.showInformationMessage("Virtual environment set up successfully!");
                            console.log("Setup script output:", setupStdout);
                        }
                    });

            }
        });
    } else {
        vscode.window.showInformationMessage("Project already exists!");
        console.log("Project already exists at:", projectPath);
    }
    });



    let disposable2 = vscode.commands.registerCommand('capstone-extension.runAutomatedInstrumentation', function () {
        console.log("Command Executed!");

        const terminal = vscode.window.createTerminal({
            name: "Capstone Extension",
            shellPath: "wsl.exe",  // Use WSL as the terminal shell
            shellArgs: []           // No additional arguments needed
        });
        terminal.show(); // Show the terminal

        const extensionPath = path.join(context.globalStorageUri.fsPath, "Automated-Instrumentation-of-Programs");
        const basePath = extensionPath
        const scriptPath = path.join(basePath, "Semgrep_CodeT5/tracing_statements/file_loader.py");

        // Convert Windows path to WSL path
        const wslBasePath = basePath.replace(/\\/g, '/').replace(/^([A-Za-z]):/, '/mnt/$1');


        console.log(`Ext Path (Windows): ${extensionPath}`);
        console.log(`Base Path (Windows): ${basePath}`);
        console.log(`Base Path (WSL): ${wslBasePath}`);
        console.log(`Script Path: ${scriptPath}`);

        // Run the script in WSL using the VS Code integrated terminal
        
        terminal.sendText(`
            cd '${wslBasePath}' && \
            source .venv/bin/activate && \
            cd Semgrep_CodeT5/tracing_statements && \
            python3 control_options.py
        `);
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
