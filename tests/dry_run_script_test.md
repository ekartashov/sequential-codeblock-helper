# Dry-Run Script Test

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
TARGET_DIR=/mnt/data
BACKUP_DIR=/mnt/backup

## Script
mkdir -p "${TARGET_DIR}"
echo "Created target directory"

## Dry-Run Script
# echo "Would create directory: ${TARGET_DIR}"
# echo "No actual changes made"
```

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
FILE_NAME="data.txt"
FILE_PATH="${TARGET_DIR}/${FILE_NAME}"

## Script
touch "${FILE_PATH}"
echo "Created file: ${FILE_PATH}"

## Dry-Run Script
# echo "Would create file: ${FILE_PATH}"
# echo "No actual file created"