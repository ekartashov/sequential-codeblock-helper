#!/usr/bin/env python3
"""
Sequential Codeblock Helper

This script processes Markdown files containing sequential bash codeblocks
and outputs each block with its dependencies as preset variables.
"""

import sys
import os
import re
import argparse
import tempfile
from typing import Dict, List, Set, Tuple, Optional


class SequentialCodeblockHelper:
    def __init__(self, use_color: bool = True):
        self.use_color = use_color
        self.variables: Dict[str, str] = {}  # All variables defined across blocks
        self.block_count = 0
        
        # ANSI color codes
        self.colors = {
            "header": "\033[1;36m",  # Bold Cyan
            "original": "\033[1;33m",  # Bold Yellow
            "deps": "\033[1;32m",  # Bold Green
            "separator": "\033[1;35m",  # Bold Magenta
            "reset": "\033[0m",
        } if use_color else {"header": "", "original": "", "deps": "", "separator": "", "reset": ""}

    def parse_markdown(self, content: str) -> List[str]:
        """Extract sequential code blocks from markdown content."""
        # Regex to find code blocks with SEQUENTIAL_CODEBLOCK comment
        pattern = r'```(?:bash|sh)(?:\s+)?<!-- SEQUENTIAL_CODEBLOCK -->\n(.*?)```'
        return re.findall(pattern, content, re.DOTALL)
    
    def extract_sections(self, block: str) -> Dict[str, str]:
        """Extract sections from a code block."""
        sections = {}
        
        # Extract Preset Variables section if present
        preset_match = re.search(r'## Preset Variables\n(.*?)(?=\n##|\Z)', block, re.DOTALL)
        if preset_match:
            sections['preset'] = preset_match.group(1).strip()
            
        # Extract Variables section
        vars_match = re.search(r'## Variables\n(.*?)(?=\n##|\Z)', block, re.DOTALL)
        if vars_match:
            sections['variables'] = vars_match.group(1).strip()
            
        # Extract Script section or Dry-Run Script section
        script_match = re.search(r'## (?:Dry-Run )?Script\n(.*?)(?=\n##|\Z)', block, re.DOTALL)
        if script_match:
            sections['script'] = script_match.group(1).strip()
            
        return sections
    
    def extract_variable_defs(self, variables_section: str) -> Dict[str, str]:
        """Extract variable definitions from the Variables section."""
        defs = {}
        if not variables_section:
            return defs
            
        for line in variables_section.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Extract variable name and its value
            match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=(.*?)$', line)
            if match:
                var_name, var_value = match.groups()
                defs[var_name] = var_value
                
        return defs
    
    def extract_variable_refs(self, block: str) -> Set[str]:
        """Extract variable references from a block."""
        # Find all $VAR or ${VAR} patterns
        refs = set()
        
        # Pattern for ${VAR} style
        for match in re.finditer(r'\${([A-Za-z_][A-Za-z0-9_]*)}', block):
            refs.add(match.group(1))
            
        # Pattern for $VAR style
        for match in re.finditer(r'(?<!\$)\$([A-Za-z_][A-Za-z0-9_]*)(?!\w)', block):
            refs.add(match.group(1))
            
        return refs
    
    def get_dependencies(self, block: str, block_defs: Dict[str, str]) -> Dict[str, str]:
        """Get variable dependencies for a block."""
        # Variables referenced in this block
        all_refs = self.extract_variable_refs(block)
        
        # Remove refs that are defined in this block
        external_refs = all_refs - set(block_defs.keys())
        
        # Find definitions from previously defined variables
        deps = {}
        for var in external_refs:
            if var in self.variables:
                deps[var] = self.variables[var]
                
        return deps
    
    def print_separator(self, text: str, char: str, width: int = 80):
        """Print a separator line with text in the middle."""
        text_len = len(text)
        left_pad = 10
        right_pad = width - left_pad - text_len
        
        separator = char * left_pad + text + char * right_pad
        print(f"{self.colors['separator']}{separator}{self.colors['reset']}")
    
    def process_block(self, block: str) -> None:
        """Process a single code block."""
        self.block_count += 1
        block_header = f" Block {self.block_count} "
        
        # Extract sections
        sections = self.extract_sections(block)
        
        # Extract variable definitions from this block
        if 'variables' in sections:
            block_defs = self.extract_variable_defs(sections['variables'])
            
            # Add to global variables
            self.variables.update(block_defs)
        else:
            block_defs = {}
            
        # Get dependencies for this block
        deps = self.get_dependencies(block, block_defs)
        
        # Print block header
        self.print_separator(block_header, "=")
        
        # Print original block
        print(f"{self.colors['original']}## Original Block: {'+' * 43}{self.colors['reset']}")
        print()
        for section_name, content in sections.items():
            if section_name == 'preset':
                print(f"## Preset Variables")
                print(f"{content}")
            elif section_name == 'variables':
                print(f"## Variables")
                print(f"{content}")
            elif section_name == 'script':
                print(f"## Script")
                print(f"{content}")
            print()
            
        # Print block with dependencies
        print(f"{self.colors['deps']}## With Dependencies: {'+' * 43}{self.colors['reset']}")
        print()
        
        if not deps:
            if 'preset' not in sections:
                print("(None Found, Identical Block)")
                print()
            else:
                # Just print the original preset section
                print(f"## Preset Variables")
                print(f"{sections['preset']}")
                print()
                print(f"## Variables")
                print(f"{sections.get('variables', '')}")
                print()
                print(f"## Script")
                print(f"{sections.get('script', '')}")
        else:
            # Print with dependencies
            print(f"## Preset Variables")
            for var, value in deps.items():
                print(f"# {var}={value}")
            print()
            
            if 'variables' in sections:
                print(f"## Variables")
                print(f"{sections['variables']}")
            
            if 'script' in sections:
                print(f"## Script")
                print(f"{sections['script']}")
        
        # Print block footer
        print(f"{self.colors['separator']}{'+' * 80}{self.colors['reset']}")
        print()
    
    def process_file(self, file_path: str) -> None:
        """Process a markdown file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Extract code blocks
            blocks = self.parse_markdown(content)
            
            # Process each block
            for block in blocks:
                self.process_block(block)
                
            # Print final summary
            print(f"{self.colors['separator']}{'=' * 80}{self.colors['reset']}")
            print(f"Total blocks: {self.block_count}")
            print(f"{self.colors['separator']}{'=' * 80}{self.colors['reset']}")
            
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error processing file: {str(e)}", file=sys.stderr)
            sys.exit(1)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Process sequential code blocks in Markdown files.")
    parser.add_argument("input_file", help="Path to the Markdown file containing sequential code blocks")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--format", "-f", choices=["text", "markdown", "html"], default="text",
                       help="Output format (default: text)")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output (for text format)")
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    if args.output:
        sys.stdout = open(args.output, 'w')
        
    # Create and run the processor
    processor = SequentialCodeblockHelper(use_color=not args.no_color)
    processor.process_file(args.input_file)
    
    if args.output:
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        print(f"Output written to {args.output}")


if __name__ == "__main__":
    main()