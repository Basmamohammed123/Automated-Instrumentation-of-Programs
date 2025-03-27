# Automated Instrumentation README

The Automated Instrumentation Extension for VS Code enhances the development process by automating the instrumentation of Python programs. This extension enables easy integration of code coverage analysis, variable tracing, and function call graph generation into your Python projects. It automatically tracks the execution flow, collects valuable runtime information, and generates detailed reports, making it easier for developers to identify untested code paths, debug issues, and optimize performance. With this extension, you can improve both the quality and efficiency of your development workflow.

## Features

The Automated Instrumentation Extension offers the following key features to enhance your Python development workflow:

Setup Code Analysis
Prepares the environment by downloading all necessary dependencies and scripts to set up the automated instrumentation process. This command ensures everything is ready for code analysis, enabling you to focus on your development without worrying about setup.

Trace Variables
Tracks and records the values of variables as the program executes, capturing data changes throughout runtime. This provides real-time insights into variable states, helping identify unexpected behavior or bugs.

Create Call Graph
Constructs a dynamic function call graph by tracing caller-callee relationships. This visual representation of function interactions can assist with understanding the execution flow and optimizing the structure of your code.

Analyze Code Coverage
Monitors and reports which lines of code are executed during the program's execution. The command identifies unexecuted paths, providing visibility into areas of the code that may need further testing.

Generate Tracing Statements
Automatically injects tracing logs into the code to capture function calls and their parameters during execution. This helps in tracking the flow of the program and debugging issues by providing detailed traces of runtime activity.



## Requirements

To use the Automated Instrumentation Extension, the following dependencies are required:

1. Visual Studio Code
The extension is designed to work within the Visual Studio Code environment. Ensure you have the latest version of VS Code installed.

2. Python 3.7+
Python 3.7 or newer is required for running the code analysis and instrumentation scripts. Ensure Python is installed and available in your system's PATH.

3. Git
Git is required for managing and versioning the extension's source code. Ensure Git is installed on your system.


## Instructions
Follow these steps to install and set up the Automated Instrumentation Extension in Visual Studio Code:

1. Install the Extension
Open Visual Studio Code and go to the Extensions view (Ctrl+Shift+X or Cmd+Shift+X on macOS).

Search for Automated Instrumentation Extension and click Install.

2. Run the Setup Command
Once the extension is installed, you need to set up the virtual environment:

Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on macOS).

Search for and select the command: Automated Instrumentation: Setup Environment.

The extension will now set up the virtual environment. You will see a notification once the setup is complete. 

### Important: Wait for the "Virtual environment setup complete!" notification before proceeding. Do not proceed with any further actions until this notification appears.

3. Use the Extension
Once the setup is complete, you can start using the extension.