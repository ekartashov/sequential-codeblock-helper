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
    def __init__(self, use_color: bool = True, output_format: str = "text"):
        self.use_color = use_color and output_format == "text"
        self.output_format = output_format
        self.variables: Dict[str, str] = {}  # All variables defined across blocks
        self.block_count = 0
        
        # ANSI color codes
        self.colors = {
            "header": "\033[1;36m",  # Bold Cyan
            "original": "\033[1;33m",  # Bold Yellow
            "deps": "\033[1;32m",  # Bold Green
            "separator": "\033[1;35m",  # Bold Magenta
            "reset": "\033[0m",
        } if self.use_color else {"header": "", "original": "", "deps": "", "separator": "", "reset": ""}

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
            
        # Extract Script section
        script_match = re.search(r'## Script\n(.*?)(?=\n##|\Z)', block, re.DOTALL)
        if script_match:
            sections['script'] = script_match.group(1).strip()
            
        # Extract Dry-Run Script section separately
        dry_run_match = re.search(r'## Dry-Run Script\n(.*?)(?=\n##|\Z)', block, re.DOTALL)
        if dry_run_match:
            sections['dry_run_script'] = dry_run_match.group(1).strip()
            
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
        
    def expand_variables(self, value: str, all_vars: Dict[str, str], depth: int = 10) -> str:
        """Recursively expand variables in a string."""
        if depth <= 0:  # Prevent infinite recursion
            return value
        
        # Check if the value contains any variable references
        has_vars = re.search(r'\${[A-Za-z_][A-Za-z0-9_]*}|\$[A-Za-z_][A-Za-z0-9_]*(?!\w)', value)
        if not has_vars:
            return value
            
        # Expand ${VAR} style variables
        for var_name in re.finditer(r'\${([A-Za-z_][A-Za-z0-9_]*)}', value):
            name = var_name.group(1)
            if name in all_vars:
                placeholder = f"${{{name}}}"
                # Recursively expand the variable's value first
                expanded_var = self.expand_variables(all_vars[name], all_vars, depth - 1)
                value = value.replace(placeholder, expanded_var)
                
        # Expand $VAR style variables
        for var_name in re.finditer(r'(?<!\$)\$([A-Za-z_][A-Za-z0-9_]*)(?!\w)', value):
            name = var_name.group(1)
            if name in all_vars:
                placeholder = f"${name}"
                # Recursively expand the variable's value first
                expanded_var = self.expand_variables(all_vars[name], all_vars, depth - 1)
                value = value.replace(placeholder, expanded_var)
                
        return value
    
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
    
    def get_dependencies(self, sections: Dict[str, str], block_defs: Dict[str, str]) -> Dict[str, str]:
        """Get variable dependencies for a block, including all referenced variables and their definitions."""
        
        # Variables referenced in the current block's script and variable sections
        # (excluding those defined within the block itself)
        current_block_content_for_refs = sections.get('script', '') + "\n" + sections.get('variables', '')
        all_refs_in_current_block = self.extract_variable_refs(current_block_content_for_refs)
        
        # Filter out variables defined in the current block's "Variables" section
        external_refs = all_refs_in_current_block - set(block_defs.keys())

        # Use a list to maintain order and a set for quick lookups
        ordered_deps_list: List[Tuple[str, str]] = []
        deps_added_set: Set[str] = set()

        def find_and_add_deps_recursively(var_names_to_process: Set[str]):
            # Process a copy of the set to allow modification during iteration
            for var_name in list(var_names_to_process):
                if var_name in self.variables and var_name not in deps_added_set:
                    var_value = self.variables[var_name]
                    
                    # Find dependencies of this variable's value
                    nested_deps_in_value = self.extract_variable_refs(var_value)
                    
                    # Recursively add dependencies of the current variable's value first
                    # This ensures that variables are defined before they are used in other definitions
                    find_and_add_deps_recursively(nested_deps_in_value - deps_added_set - set(block_defs.keys()))
                    
                    # Add the current variable if it hasn't been added yet
                    if var_name not in deps_added_set:
                        ordered_deps_list.append((var_name, var_value))
                        deps_added_set.add(var_name)
        
        # Start the recursive search with the initial external references
        find_and_add_deps_recursively(external_refs)
        
        # Convert the list of tuples to a dictionary for the return type
        # The order is preserved by how items were added to ordered_deps_list
        return dict(ordered_deps_list)
    
    def print_separator(self, text: str, char: str, width: int = 80):
        """Print a separator line with text in the middle."""
        text_len = len(text)
        left_pad = 10
        right_pad = width - left_pad - text_len
        
        # If it's the original block header, we need to make this a special case
        if text == "Original Block: ":
            # The original title's content plus a special marker
            original_title_suffix = "+" * 43
            separator = char * left_pad + text + original_title_suffix
        else:
            separator = char * left_pad + text + char * (width - left_pad - text_len)
            
        if self.output_format == "text":
            print(f"{self.colors['separator']}{separator}{self.colors['reset']}")
        elif self.output_format == "markdown":
            if text.strip():  # If it's a header with text
                print(f"### {text.strip()}")
            else:  # Just a separator
                print("\n---\n")
        elif self.output_format == "html":
            if "Block" in text:  # Block header
                print(f"<h3 class='block-header'>{text}</h3>")
            elif text == "Original Block: " or text == "With Dependencies: ":
                print(f"<h4 class='section-header'>{text}</h4>")
            else:  # Just a separator
                print("<hr>")
    
    def process_block(self, block: str) -> None:
        """Process a single code block."""
        self.block_count += 1
        block_header = f" Block {self.block_count} "
        
        # Extract sections
        sections = self.extract_sections(block)
        
        # Extract variable definitions from this block
        if 'variables' in sections:
            block_defs = self.extract_variable_defs(sections['variables'])
            
            # Expand any variables that might reference previously defined variables
            expanded_defs = {}
            for var_name, var_value in block_defs.items():
                expanded_defs[var_name] = self.expand_variables(var_value, self.variables)
            
            # Add to global variables
            self.variables.update(expanded_defs)
        else:
            block_defs = {}
            
        # Get dependencies for this block
        deps = self.get_dependencies(sections, block_defs)
        
        # Print block header
        self.print_separator(block_header, "=")
        
        # Print original block
        if self.output_format == "text":
            print(f"{self.colors['original']}## Original Block: {self.colors['reset']}")
        elif self.output_format == "markdown":
            print("#### Original Block")
            print("```bash")
        elif self.output_format == "html":
            print("<div class='original-block'>")
            print("<h4>Original Block</h4>")
            print("<pre><code>")
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
            elif section_name == 'dry_run_script':
                print(f"## Dry-Run Script")
                print(f"{content}")
            print()
        
        if self.output_format == "markdown":
            print("```")
        elif self.output_format == "html":
            print("</code></pre>")
            print("</div>")
            
        # Print block with dependencies
        if self.output_format == "text":
            print(f"{self.colors['deps']}## With Dependencies: {self.colors['reset']}")
        elif self.output_format == "markdown":
            print("#### With Dependencies")
            print("```bash")
        elif self.output_format == "html":
            print("<div class='dependencies-block'>")
            print("<h4>With Dependencies</h4>")
            print("<pre><code>")
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
                
                if 'variables' in sections:
                    print(f"## Variables")
                    print(f"{sections['variables']}")
                    print()
                
                if 'script' in sections:
                    print(f"## Script")
                    print(f"{sections['script']}")
                    print()
                
                if 'dry_run_script' in sections:
                    print(f"## Dry-Run Script")
                    print(f"{sections['dry_run_script']}")
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
                
            if 'dry_run_script' in sections:
                print(f"## Dry-Run Script")
                print(f"{sections['dry_run_script']}")
        
        if self.output_format == "markdown":
            print("```")
        elif self.output_format == "html":
            print("</code></pre>")
            print("</div>")
            
        # Print block footer
        if self.output_format == "text":
            # Ensure separator is exactly 80 chars (not including ANSI color codes)
            footer = '+' * 80
            print(f"{self.colors['separator']}{footer}{self.colors['reset']}")
        elif self.output_format == "markdown":
            print("\n---\n")
        elif self.output_format == "html":
            print("<hr class='block-separator'>")
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
                # No longer updating variables with expansions globally
                
            # Print final summary
            if self.output_format == "text":
                # Ensure separator is exactly 80 chars
                separator = '=' * 80
                print(f"{self.colors['separator']}{separator}{self.colors['reset']}")
                print(f"Total blocks: {self.block_count}")
                print(f"{self.colors['separator']}{separator}{self.colors['reset']}")
            elif self.output_format == "markdown":
                print(f"**Total blocks: {self.block_count}**")
                print("\n---\n")
            elif self.output_format == "html":
                print("<div class='summary'>")
                print(f"<p><strong>Total blocks: {self.block_count}</strong></p>")
                print("</div>")
                print("<hr>")
            
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
    processor = SequentialCodeblockHelper(use_color=not args.no_color, output_format=args.format)
    processor.process_file(args.input_file)
    
    if args.output:
        sys.stdout.close()
        sys.stdout = sys.__stdout__
        print(f"Output written to {args.output}")


if __name__ == "__main__":
    main()