# Recursive Variable Expansion Test

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
BASE_DIR=/opt/app
CONFIG_PATH=${BASE_DIR}/config
LOG_PATH=${BASE_DIR}/logs
NESTED_CONFIG=${CONFIG_PATH}/settings.conf

## Script
echo "Final path: ${NESTED_CONFIG}"
```

```bash <!-- SEQUENTIAL_CODEBLOCK -->
## Variables
DATA_DIR=${BASE_DIR}/data
NESTED_DATA=${DATA_DIR}/cache
DOUBLE_NESTED=${NESTED_DATA}/temp

## Script
mkdir -p "${DOUBLE_NESTED}"
echo "Created directory: ${DOUBLE_NESTED}"
```