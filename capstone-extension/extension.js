const vscode = require('vscode');
const path = require('path');

function activate(context) {

    console.log("Capstone Extension Active!");

    let disposable = vscode.commands.registerCommand('capstone-extension.runPython', function () { 
        console.log("Command Executed!");

        const terminal = vscode.window.createTerminal("Capstone Extension");
        terminal.show(); // Show the terminal

        const extensionPath = __dirname; 
        const basePath = path.resolve(extensionPath, "..");
        const scriptPath = path.join(basePath, "Semgrep_CodeT5/tracing_statements/delete_soon.py");

        // Convert Windows path to WSL path
        const wslBasePath = basePath.replace(/\\/g, '/').replace(/^([A-Za-z]):/, '/mnt/$1');

        
        console.log(`Base Path (Windows): ${basePath}`);
        console.log(`Base Path (WSL): ${wslBasePath}`);
        console.log(`Script Path: ${scriptPath}`);

        // Run the script in WSL using the VS Code integrated terminal
        terminal.sendText(`
            wsl bash -c "
            cd '${wslBasePath}' && \
            source .venv/bin/activate && \
            cd Semgrep_CodeT5/tracing_statements && \
            python3 delete_soon.py
            "
        `);
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
