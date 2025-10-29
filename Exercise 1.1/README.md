# TestScripts Project

This project demonstrates Python virtual environment setup, package management, and basic Python scripting.

## Project Structure

```
TestScripts/
├── README.md                 # This documentation file
├── requirements.txt          # Python package dependencies
├── add.py                   # Simple addition calculator script
├── hello.py                 # Basic Python script
├── cf-python-base/          # Primary virtual environment
└── cf-python-copy/          # Secondary virtual environment (for testing)
```

## Virtual Environments

### cf-python-base
The primary virtual environment containing:
- Python 3.14.0
- IPython 9.6.0 (enhanced Python shell with syntax highlighting and auto-completion)
- All IPython dependencies

### cf-python-copy
A secondary environment created to demonstrate the requirements.txt workflow by installing the same packages as cf-python-base.

## Scripts

### add.py
A simple Python script that:
- Prompts the user for two numbers
- Adds them together
- Displays the result

**Usage:**
```bash
python add.py
```

### hello.py
A basic Python script (existing file in the workspace).

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv cf-python-base
```

### 2. Activate Environment
```bash
source cf-python-base/bin/activate
```

### 3. Install IPython
```bash
pip install ipython
```

### 4. Generate Requirements File
```bash
pip freeze > requirements.txt
```

### 5. Create Copy Environment (Optional)
```bash
python3 -m venv cf-python-copy
source cf-python-copy/bin/activate
pip install -r requirements.txt
```

## Package Dependencies

The project uses the following Python packages (as listed in requirements.txt):

- **ipython==9.6.0** - Enhanced interactive Python shell
- **asttokens==3.0.0** - Annotate Python AST trees with source text
- **decorator==5.2.1** - Better living through Python decorators
- **executing==2.2.1** - Get information about what a Python frame is currently executing
- **jedi==0.19.2** - Awesome autocompletion library for Python
- **matplotlib-inline==0.2.1** - Inline backend for Matplotlib
- **parso==0.8.5** - Python parser supporting different Python versions
- **pexpect==4.9.0** - Cross-platform expect module
- **prompt_toolkit==3.0.52** - Library for building interactive command line applications
- **ptyprocess==0.7.0** - Cross-platform wrapper for subprocess
- **pure_eval==0.2.3** - Safely evaluate Python expressions
- **Pygments==2.19.2** - Syntax highlighting package
- **stack-data==0.6.3** - Extract data from Python stack frames
- **traitlets==5.14.3** - Configuration system for Python applications
- **wcwidth==0.2.14** - Measure number of terminal column cells

## Usage Examples

### Running the Addition Script
```bash
# Activate environment
source cf-python-base/bin/activate

# Run the script
python add.py

# Example interaction:
# Enter the first number: 5
# Enter the second number: 3
# 8
```

### Using IPython Shell
```bash
# Activate environment
source cf-python-base/bin/activate

# Launch IPython
ipython

# Features include:
# - Syntax highlighting
# - Auto-indentation  
# - Robust auto-completion
# - Magic commands
```

## Requirements.txt Workflow

This project demonstrates the complete requirements.txt workflow:

1. **Generate**: `pip freeze > requirements.txt` captures all installed packages
2. **Share**: The requirements.txt file can be shared with the project
3. **Reproduce**: `pip install -r requirements.txt` recreates the exact environment
4. **Deploy**: Ensures consistent environments across different systems

## Environment Management

### Activating Environments
```bash
# Activate cf-python-base
source cf-python-base/bin/activate

# Activate cf-python-copy  
source cf-python-copy/bin/activate
```

### Deactivating Environment
```bash
deactivate
```

### Checking Environment Status
```bash
# Check which environment is active (look for environment name in prompt)
# Check Python version
python --version

# Check installed packages
pip list
```

## System Requirements

- macOS (tested environment)
- Python 3.14.0 or compatible version
- pip package manager
- Terminal with zsh shell

## Notes

- Virtual environments keep project dependencies isolated from system Python
- The requirements.txt file ensures reproducible environments
- IPython provides enhanced features over the standard Python REPL
- All packages are pinned to specific versions for consistency

