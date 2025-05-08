# Sequential Codeblock Helper

A Python utility that processes Markdown files containing sequential bash codeblocks, making them individually executable by managing their variable dependencies.

## Overview

Sequential Codeblock Helper parses Markdown files containing bash code blocks marked with `<!-- SEQUENTIAL_CODEBLOCK -->` and processes their variable dependencies. It produces output that shows each block alongside a modified version with proper `## Preset Variables` sections to make individual blocks independently executable.

### The Problem

When writing bash instructions in Markdown files, code blocks often depend on variables defined in previous blocks. If you want to run a specific block in isolation (e.g., in a new terminal session), you need to manually track and redefine all variables from previous blocks.

### The Solution

This tool:
1. Analyzes all `<!-- SEQUENTIAL_CODEBLOCK -->` blocks in a Markdown file
2. Tracks variable definitions and dependencies between blocks
3. For each block, generates a complete `## Preset Variables` section containing all required variables
4. Outputs both the original and dependency-aware versions of each block

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sequential-codeblock-helper.git
cd sequential-codeblock-helper

# Optional: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python sequential_codeblock_helper.py path/to/example.md
```

### Options

```bash
python sequential_codeblock_helper.py --help
```

```
usage: sequential_codeblock_helper.py [-h] [--output OUTPUT] [--format {text,markdown,html}] [--no-color] input_file

Process sequential code blocks in Markdown files.

positional arguments:
  input_file            Path to the Markdown file containing sequential code blocks

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output file (default: stdout)
  --format {text,markdown,html}, -f {text,markdown,html}
                        Output format (default: text)
  --no-color            Disable colored output (for text format)
```

## Example

Input file (`example.md`):

~~~markdown
# Disk Setup Guide

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
DRIVE=/dev/sdx
## Script
parted "$DRIVE" --script \
  mklabel gpt \
  mkpart primary 1MiB 512MiB \
  mkpart primary 512MiB 100%
```

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
PART1=${DRIVE}1
PART2=${DRIVE}2
## Script
mkfs.vfat -F32 "$PART1"
mkfs.ext4 "$PART2"
```
~~~

Running the command:

```bash
python sequential_codeblock_helper.py example.md
```

Output:

```
========== Block 1 ==================================================
## Original Block: ++++++++++++++++++++++++++++++++++++++++++

## Variables
DRIVE=/dev/sdx
## Script
parted "$DRIVE" --script \
  mklabel gpt \
  mkpart primary 1MiB 512MiB \
  mkpart primary 512MiB 100%

## With Dependencies: +++++++++++++++++++++++++++++++++++++++

(None Found, Identical Block)

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

========== Block 2 ==================================================
## Original Block: ++++++++++++++++++++++++++++++++++++++++++

## Variables
PART1=${DRIVE}1
PART2=${DRIVE}2
## Script
mkfs.vfat -F32 "$PART1"
mkfs.ext4 "$PART2"

## With Dependencies: +++++++++++++++++++++++++++++++++++++++

## Preset Variables
# DRIVE=/dev/sdx

## Variables
PART1=${DRIVE}1
PART2=${DRIVE}2
## Script
mkfs.vfat -F32 "$PART1"
mkfs.ext4 "$PART2"
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Total blocks: 2
================================================================================
```

## How It Works

1. **Parsing**: The script uses regular expressions to identify sequential code blocks in Markdown files
2. **Variable Tracking**: It tracks variable definitions in each block's `## Variables` section
3. **Dependency Analysis**: For each block, it identifies which variables are used but not defined within that block
4. **Variable Resolution**: It resolves these dependencies by looking at previous blocks
5. **Output Generation**: It produces both the original block and a version with all dependencies included in the `## Preset Variables` section

### Variable Detection

The script detects:
- Simple variable assignments (`VAR=value`)
- Command substitution (`VAR=$(command)`)
- Variable references (`${VAR}` or `$VAR`)
- Array variables (`ARRAY=(item1 item2)`)
- Associative arrays (`declare -A ASSOC=([key1]=value1 [key2]=value2)`)

## Project Structure

```
sequential-codeblock-helper/
├── README.md
├── sequential_codeblock_helper.py   # Main script
├── requirements.txt                # Dependencies
├── tests/                          # Test files
│   ├── test_sequential_codeblock_helper.py
│   └── fixtures/                   # Test input files
│       ├── simple_example.md
│       └── complex_example.md
└── examples/                       # Example markdown files
    └── example.md                  # The example file used in this README
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
