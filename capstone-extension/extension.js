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
        vscode.window.showInformationMessage("Downloading Resources , please wait...");
        exec(`git clone https://github.com/Basmamohammed123/Automated-Instrumentation-of-Programs.git ${projectPath}`, (err, stdout, stderr) => {
            if (err) {
                vscode.window.showErrorMessage("Failed to clone project: " + stderr);
            } else {
                vscode.window.showInformationMessage("Download Complete");
                console.log("Project cloned successfully:", stdout);

                const setupScriptPath = path.join(projectPath, "setup-venv.ps1");
                vscode.window.showInformationMessage("Installing content. This may take a while!" , setupScriptPath);
                
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


    function runPythonScript(scriptName) {
            console.log(`Running: ${scriptName}`);

            const terminal = vscode.window.createTerminal({
                name: "Capstone Extension",
                shellPath: "wsl.exe",
                shellArgs: []
            });
            terminal.show();

            const extensionPath = path.join(context.globalStorageUri.fsPath, "Automated-Instrumentation-of-Programs");
            const basePath = extensionPath;

            const copyScriptPath = path.join(basePath, "Semgrep_CodeT5/tracing_statements/copy_contents.py");

            const activeEditor = vscode.window.activeTextEditor;
            if (!activeEditor) {
                vscode.window.showErrorMessage("No active editor!");
                return;
            }

            const currentFile = activeEditor.document.uri.fsPath;
            const currentDir = path.dirname(currentFile);

            const wslBasePath = basePath.replace(/\\/g, '/').replace(/^([A-Za-z]):/, '/mnt/$1');
            const wslCurrentFile = currentFile.replace(/\\/g, '/').replace(/^([A-Za-z]):/, '/mnt/$1');
            const wslOutputPath = `${wslCurrentFile.replace(/\.py$/, '')}_trace_output.txt`;

            // Logs for debugging
            console.log(`Base Path (Windows): ${basePath}`);
            console.log(`Base Path (WSL): ${wslBasePath}`);
            console.log(`Current File (WSL): ${wslCurrentFile}`);
            console.log(`Trace Output (WSL): ${wslOutputPath}`);

            terminal.sendText(`
                cd '${wslBasePath}' && \
                source .venv/bin/activate && \
                cd Semgrep_CodeT5/tracing_statements && \
                python3 copy_contents.py '${wslCurrentFile}' && \
                python3 ${scriptName} '${wslCurrentFile}' '${wslOutputPath}'
            `);
        }


        const commands = [
            { name: 'extension.generateTracing', script: 'generate_tracing_statements.py', message: 'Generating Tracing Statements...' },
            { name: 'extension.createCallGraph', script: 'generate_call_graph.py', message: 'Creating Call Graph...' },
            { name: 'extension.traceVariables', script: `variable_tracer.py `, message: 'Tracing Variables...' },
            { name: 'extension.analyzeCodeCoverage', script: 'runtime_coverage.py', message: 'Analyzing Code Coverage...' }
        ];

        commands.forEach(cmd => {
            const disposable = vscode.commands.registerCommand(cmd.name, () => {
                vscode.window.showInformationMessage(cmd.message);
                runPythonScript(cmd.script);
            });
            context.subscriptions.push(disposable);
        });

}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
