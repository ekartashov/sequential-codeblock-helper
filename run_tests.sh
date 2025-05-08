#!/bin/bash
# Test script for Sequential Codeblock Helper

echo "==== Testing Sequential Codeblock Helper ===="
echo

# Create a temp directory for test outputs
TEMP_DIR=$(mktemp -d)

echo "Testing with example.md (default output):"
python3 sequential_codeblock_helper.py example.md > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ Success: Default test passed"
else
  echo "❌ Error: Default test failed"
fi
echo

echo "Testing with no-color option:"
python3 sequential_codeblock_helper.py --no-color example.md > /dev/null
if [ $? -eq 0 ]; then
  echo "✅ Success: No-color test passed"
else
  echo "❌ Error: No-color test failed"
fi
echo

echo "Testing with output file:"
python3 sequential_codeblock_helper.py -o "${TEMP_DIR}/test_output.txt" example.md
if [ $? -eq 0 ] && [ -f "${TEMP_DIR}/test_output.txt" ]; then
  echo "✅ Success: Output file test passed"
else
  echo "❌ Error: Output file test failed"
fi
echo

# ===== Testing fixed issues =====

echo "Testing recursive variable definitions:"
# Use the --no-color option to make grep matching more reliable
python3 sequential_codeblock_helper.py tests/recursive_vars_test.md --no-color -o "${TEMP_DIR}/recursive_vars.txt"
if [ $? -eq 0 ] && [ -f "${TEMP_DIR}/recursive_vars.txt" ]; then
  # The second block's "With Dependencies" section should list BASE_DIR
  # We can check for the line "# BASE_DIR=/opt/app" within the second block's output.
  # A simple way is to find "Block 2" and then check the subsequent lines for the dependency.
  if awk '/========== Block 2 ==========/ {f=1} f && /# BASE_DIR=\/opt\/app/ {print; exit}' "${TEMP_DIR}/recursive_vars.txt" | grep -q "# BASE_DIR=/opt/app"; then
    echo "✅ Success: Recursive variable definitions test passed"
  else
    echo "❌ Error: Recursive variable definitions test failed"
    echo "BASE_DIR not properly included as a dependency for the second block."
  fi
else
  echo "❌ Error: Recursive variable definitions test failed"
fi
echo

echo "Testing Dry-Run Script separation:"
python3 sequential_codeblock_helper.py tests/dry_run_script_test.md -o "${TEMP_DIR}/dry_run.txt"
if [ $? -eq 0 ] && [ -f "${TEMP_DIR}/dry_run.txt" ]; then
  # Check if Dry-Run Script sections are properly separated
  if grep -q "## Dry-Run Script" "${TEMP_DIR}/dry_run.txt"; then
    echo "✅ Success: Dry-Run Script separation test passed"
  else
    echo "❌ Error: Dry-Run Script separation test failed"
  fi
else
  echo "❌ Error: Dry-Run Script separation test failed"
fi
echo

echo "Testing format options:"
# Test text format
python3 sequential_codeblock_helper.py tests/format_options_test.md --format text -o "${TEMP_DIR}/format_text.txt"
# Test markdown format
python3 sequential_codeblock_helper.py tests/format_options_test.md --format markdown -o "${TEMP_DIR}/format_md.md"
# Test html format
python3 sequential_codeblock_helper.py tests/format_options_test.md --format html -o "${TEMP_DIR}/format_html.html"

if [ $? -eq 0 ] && [ -f "${TEMP_DIR}/format_text.txt" ] &&
   [ -f "${TEMP_DIR}/format_md.md" ] && [ -f "${TEMP_DIR}/format_html.html" ]; then
  # Check text format
  if grep -q "=========" "${TEMP_DIR}/format_text.txt"; then
    TEXT_OK=true
  else
    TEXT_OK=false
  fi
  
  # Check markdown format
  if grep -q "\`\`\`bash" "${TEMP_DIR}/format_md.md"; then
    MD_OK=true
  else
    MD_OK=false
  fi
  
  # Check html format
  if grep -q "<div" "${TEMP_DIR}/format_html.html"; then
    HTML_OK=true
  else
    HTML_OK=false
  fi
  
  if $TEXT_OK && $MD_OK && $HTML_OK; then
    echo "✅ Success: Format options test passed"
  else
    echo "❌ Error: Format options test failed"
    [ $TEXT_OK ] || echo "  - Text format failed"
    [ $MD_OK ] || echo "  - Markdown format failed"
    [ $HTML_OK ] || echo "  - HTML format failed"
  fi
else
  echo "❌ Error: Format options test failed"
fi
echo

echo "Testing separator lengths:"
# Use no-color option to avoid ANSI color codes affecting the length
python3 sequential_codeblock_helper.py tests/format_options_test.md --no-color -o "${TEMP_DIR}/separator_test.txt"

# Check if separators are exactly 80 characters in length
SEP_COUNT=$(grep -c "=========" "${TEMP_DIR}/separator_test.txt" 2>/dev/null || echo "0")
if [ $SEP_COUNT -gt 0 ]; then
  # Check the length of separator lines
  SEP_LINE=$(grep "==========" "${TEMP_DIR}/separator_test.txt" | head -1)
  if [ ${#SEP_LINE} -eq 80 ]; then
    echo "✅ Success: Separator length test passed"
  else
    echo "❌ Error: Separator length test failed (length: ${#SEP_LINE}, expected: 80)"
  fi
else
  echo "❌ Error: Separator length test failed (no separators found)"
fi
echo

# Clean up
rm -rf "${TEMP_DIR}"

echo "==== All tests completed ===="