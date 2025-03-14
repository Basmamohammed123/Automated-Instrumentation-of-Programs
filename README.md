

## How to Install and Use:
1. In the terminal, add an Ubuntu (WSL) terminal.
2. Create a new virtual environment:
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
3. Navigate to the `Merge` folder.
4. Run `merge.py` with the following command:
   - `python3 merge.py`

**Note**: Make sure you have all the required dependencies installed:
- `pip install transformers datasets torch`

## Features:
- Automatically generates tracing statements.
- Creates call graphs.
- Provides runtime coverage for the code.

## Requirements:
- Python 3
- WSL (Windows Subsystem for Linux)
