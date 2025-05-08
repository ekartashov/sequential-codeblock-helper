# Format Options Test

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
TEST_DIR=/tmp/test
FORMAT_NAME="example"

## Script
echo "Testing format options"
mkdir -p "${TEST_DIR}"
```

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
OUTPUT_FILE="${TEST_DIR}/${FORMAT_NAME}.txt"

## Script
echo "Format test content" > "${OUTPUT_FILE}"
echo "Created ${OUTPUT_FILE}"