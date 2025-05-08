# Decision Log

This file records architectural and implementation decisions...

*
[2025-05-08 18:42:26] - ## Design Decisions

### Parser Approach
Decided to use regular expressions for parsing sequential codeblocks instead of a full markdown parser. This approach is simpler and more focused on our specific needs of extracting blocks with the `<!-- SEQUENTIAL_CODEBLOCK -->` marker. A full markdown parser would be overkill and introduce unnecessary dependencies.

### Variable Detection Strategy
Implemented two-phase variable detection:
1. First phase extracts explicit variable definitions (`VAR=value` format) from `## Variables` sections
2. Second phase identifies variable references (`$VAR` and `${VAR}` formats) in the entire block

This approach allows us to correctly identify dependencies even when variables are used in complex ways or nested inside other expressions.

### Output Format
Chose a structured format that clearly separates:
- Original block content
- Dependencies section with preset variables

This makes it immediately clear which variables need to be defined for a block to run independently. Used visual separators and optional color coding to improve readability.

### Implementation Language
Chose Python for its strong text processing capabilities, cross-platform compatibility, and ease of installation. Python's regex support and string manipulation functions are well-suited for this type of parsing task.

[2025-05-08 21:27:17] - Refactored the `get_dependencies` method in `sequential_codeblock_helper.py` to recursively include the definitions of all referenced variables, rather than their expanded values. This ensures that variables are listed in the correct order in the 'Preset Variables' section. Updated tests to reflect this change.
