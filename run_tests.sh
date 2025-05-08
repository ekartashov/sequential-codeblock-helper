#!/bin/bash
# Simple test script for Sequential Codeblock Helper

echo "==== Testing Sequential Codeblock Helper ===="
echo

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
python3 sequential_codeblock_helper.py -o test_output.txt example.md
if [ $? -eq 0 ] && [ -f test_output.txt ]; then
  echo "✅ Success: Output file test passed"
  rm test_output.txt
else
  echo "❌ Error: Output file test failed"
fi
echo

echo "==== All tests completed ===="