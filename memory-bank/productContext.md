# Product Context

This file provides a high-level overviewbased on project brief:

# Sequential Codeblock Helper

This project is a Python utility that processes Markdown files containing sequential bash codeblocks, making them individually executable by managing their variable dependencies.

The tool analyzes markdown files for `<!-- SEQUENTIAL_CODEBLOCK -->` blocks, tracks variable definitions and dependencies between blocks, and generates output showing both the original blocks and versions with complete `## Preset Variables` sections for standalone execution.

The problem it solves is that when writing bash instructions in Markdown files, code blocks often depend on variables defined in previous blocks. This tool makes it possible to run any block in isolation by automatically tracking and including all required variable dependencies.

...

*