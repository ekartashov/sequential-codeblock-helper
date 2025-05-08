### Block 1
#### Original Block
```bash

## Variables
DRIVE=/dev/sdx
TARGET_SIZE="100G"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Script
# Create a new GPT partition table and two partitions
echo "Creating partition table on $DRIVE" | tee -a "$LOG_FILE"
parted "$DRIVE" --script \
  mklabel gpt \
  mkpart primary 1MiB 512MiB \
  mkpart primary 512MiB 100%

# Verify partitions were created
echo "Verifying partitions:" | tee -a "$LOG_FILE"
parted "$DRIVE" --script print

```
#### With Dependencies
```bash

(None Found, Identical Block)

```

---


### Block 2
#### Original Block
```bash

## Preset Variables
# DRIVE=/dev/sdx
# TARGET_SIZE="100G"
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
PART1=${DRIVE}1
PART2=${DRIVE}2
PARTITION_COUNT=$(lsblk "$DRIVE" | grep -c part)

## Script
# Verify we have exactly 2 partitions
if [ "$PARTITION_COUNT" -ne 2 ]; then
  echo "ERROR: Expected 2 partitions, found $PARTITION_COUNT" | tee -a "$LOG_FILE"
  exit 1
fi

# Format partitions
echo "Formatting partitions..." | tee -a "$LOG_FILE"
mkfs.vfat -F32 "$PART1"
mkfs.ext4 -L "rootfs" "$PART2"

# Show filesystem info
echo "Partition details:" | tee -a "$LOG_FILE"
blkid "$PART1" "$PART2"

```
#### With Dependencies
```bash

## Preset Variables
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# DRIVE=/dev/sdx
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
PART1=${DRIVE}1
PART2=${DRIVE}2
PARTITION_COUNT=$(lsblk "$DRIVE" | grep -c part)
## Script
# Verify we have exactly 2 partitions
if [ "$PARTITION_COUNT" -ne 2 ]; then
  echo "ERROR: Expected 2 partitions, found $PARTITION_COUNT" | tee -a "$LOG_FILE"
  exit 1
fi

# Format partitions
echo "Formatting partitions..." | tee -a "$LOG_FILE"
mkfs.vfat -F32 "$PART1"
mkfs.ext4 -L "rootfs" "$PART2"

# Show filesystem info
echo "Partition details:" | tee -a "$LOG_FILE"
blkid "$PART1" "$PART2"
```

---


### Block 3
#### Original Block
```bash

## Preset Variables
# DRIVE=/dev/sdx
# PART1=${DRIVE}1
# PART2=${DRIVE}2
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
LABEL1="BOOTFS"
LABEL2="ROOTFS"
SUCCESS=false

## Script
# Assign human-readable labels
echo "Labeling partitions..." | tee -a "$LOG_FILE"
fatlabel "$PART1" "$LABEL1"
e2label "$PART2" "$LABEL2"

# Verify labels
if blkid "$PART1" | grep -q "LABEL=\"$LABEL1\"" && blkid "$PART2" | grep -q "LABEL=\"$LABEL2\""; then
  echo "SUCCESS: Partitions labeled correctly" | tee -a "$LOG_FILE"
  SUCCESS=true
else
  echo "ERROR: Failed to set labels correctly" | tee -a "$LOG_FILE"
fi

```
#### With Dependencies
```bash

## Preset Variables
# PART1=/dev/sdx1
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# PART2=/dev/sdx2
# DRIVE=/dev/sdx
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
LABEL1="BOOTFS"
LABEL2="ROOTFS"
SUCCESS=false
## Script
# Assign human-readable labels
echo "Labeling partitions..." | tee -a "$LOG_FILE"
fatlabel "$PART1" "$LABEL1"
e2label "$PART2" "$LABEL2"

# Verify labels
if blkid "$PART1" | grep -q "LABEL=\"$LABEL1\"" && blkid "$PART2" | grep -q "LABEL=\"$LABEL2\""; then
  echo "SUCCESS: Partitions labeled correctly" | tee -a "$LOG_FILE"
  SUCCESS=true
else
  echo "ERROR: Failed to set labels correctly" | tee -a "$LOG_FILE"
fi
```

---


### Block 4
#### Original Block
```bash

## Preset Variables
# PART1=${DRIVE}1
# PART2=${DRIVE}2
# LABEL1="BOOTFS"
# LABEL2="ROOTFS"
# SUCCESS=false
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
MOUNT1="/mnt/boot"
MOUNT2="/mnt/root"
MOUNT_OPTIONS=("-o" "defaults,noatime")
MOUNT_ARRAY=("$PART1" "$PART2")
MOUNT_POINTS=("$MOUNT1" "$MOUNT2")

## Script
# Only proceed if labeling was successful
if [ "$SUCCESS" != "true" ]; then
  echo "ERROR: Previous step failed, skipping mounting" | tee -a "$LOG_FILE"
  exit 1
fi

# Create mount points
echo "Creating mount points..." | tee -a "$LOG_FILE"
mkdir -p "$MOUNT1" "$MOUNT2"

# Mount partitions
echo "Mounting partitions..." | tee -a "$LOG_FILE"
mount "${MOUNT_OPTIONS[@]}" "${MOUNT_ARRAY[0]}" "${MOUNT_POINTS[0]}"
mount "${MOUNT_OPTIONS[@]}" "${MOUNT_ARRAY[1]}" "${MOUNT_POINTS[1]}"

# Verify mounts
df -h | grep -E "$MOUNT1|$MOUNT2"

```
#### With Dependencies
```bash

## Preset Variables
# SUCCESS=false
# PART1=/dev/sdx1
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# PART2=/dev/sdx2
# DRIVE=/dev/sdx
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
MOUNT1="/mnt/boot"
MOUNT2="/mnt/root"
MOUNT_OPTIONS=("-o" "defaults,noatime")
MOUNT_ARRAY=("$PART1" "$PART2")
MOUNT_POINTS=("$MOUNT1" "$MOUNT2")
## Script
# Only proceed if labeling was successful
if [ "$SUCCESS" != "true" ]; then
  echo "ERROR: Previous step failed, skipping mounting" | tee -a "$LOG_FILE"
  exit 1
fi

# Create mount points
echo "Creating mount points..." | tee -a "$LOG_FILE"
mkdir -p "$MOUNT1" "$MOUNT2"

# Mount partitions
echo "Mounting partitions..." | tee -a "$LOG_FILE"
mount "${MOUNT_OPTIONS[@]}" "${MOUNT_ARRAY[0]}" "${MOUNT_POINTS[0]}"
mount "${MOUNT_OPTIONS[@]}" "${MOUNT_ARRAY[1]}" "${MOUNT_POINTS[1]}"

# Verify mounts
df -h | grep -E "$MOUNT1|$MOUNT2"
```

---


### Block 5
#### Original Block
```bash

## Preset Variables
# MOUNT1="/mnt/boot"
# MOUNT2="/mnt/root"
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
CONFIG_DIR="${MOUNT2}/etc/config"
SYSTEM_TYPE="server"
OPTIONS=("networking" "storage" "security")
ENABLED_FEATURES=()

## Script
# Create config directory
echo "Setting up configuration directory..." | tee -a "$LOG_FILE"
mkdir -p "$CONFIG_DIR"

# Generate system configuration based on type
cat > "${CONFIG_DIR}/system.conf" << EOF
SYSTEM_TYPE=${SYSTEM_TYPE}
SETUP_DATE=$(date +%Y-%m-%d)
HOSTNAME=example-${SYSTEM_TYPE}
EOF

# Enable selected features
for feature in "${OPTIONS[@]}"; do
  if [ "$feature" = "security" ] || [ "$feature" = "networking" ]; then
    ENABLED_FEATURES+=("$feature")
    echo "Enabling feature: $feature" | tee -a "$LOG_FILE"
    touch "${CONFIG_DIR}/${feature}.enabled"
  fi
done

echo "Enabled features: ${ENABLED_FEATURES[*]}" | tee -a "$LOG_FILE"

```
#### With Dependencies
```bash

## Preset Variables
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# MOUNT2="/mnt/root"
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
CONFIG_DIR="${MOUNT2}/etc/config"
SYSTEM_TYPE="server"
OPTIONS=("networking" "storage" "security")
ENABLED_FEATURES=()
## Script
# Create config directory
echo "Setting up configuration directory..." | tee -a "$LOG_FILE"
mkdir -p "$CONFIG_DIR"

# Generate system configuration based on type
cat > "${CONFIG_DIR}/system.conf" << EOF
SYSTEM_TYPE=${SYSTEM_TYPE}
SETUP_DATE=$(date +%Y-%m-%d)
HOSTNAME=example-${SYSTEM_TYPE}
EOF

# Enable selected features
for feature in "${OPTIONS[@]}"; do
  if [ "$feature" = "security" ] || [ "$feature" = "networking" ]; then
    ENABLED_FEATURES+=("$feature")
    echo "Enabling feature: $feature" | tee -a "$LOG_FILE"
    touch "${CONFIG_DIR}/${feature}.enabled"
  fi
done

echo "Enabled features: ${ENABLED_FEATURES[*]}" | tee -a "$LOG_FILE"
```

---


### Block 6
#### Original Block
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# CONFIG_DIR="${MOUNT2}/etc/config"
# SYSTEM_TYPE="server"
# ENABLED_FEATURES=("networking" "security")
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
SECURITY_LEVEL=${SECURITY_LEVEL:-"high"}
NETWORK_TYPE=${NETWORK_TYPE:-"bridged"}
declare -A CONFIG_VALUES=(
  [security_audit]="yes"
  [firewall]="enabled"
  [ssh_port]="2222"
)

## Script
# Configure enabled features
echo "Configuring features..." | tee -a "$LOG_FILE"

for feature in "${ENABLED_FEATURES[@]}"; do
  case "$feature" in
    networking)
      echo "Setting up $NETWORK_TYPE networking..." | tee -a "$LOG_FILE"
      cat > "${CONFIG_DIR}/network.conf" << EOF
TYPE=$NETWORK_TYPE
DHCP=yes
HOSTNAME=example-${SYSTEM_TYPE}
EOF
      ;;
    security)
      echo "Configuring $SECURITY_LEVEL security..." | tee -a "$LOG_FILE"
      cat > "${CONFIG_DIR}/security.conf" << EOF
LEVEL=$SECURITY_LEVEL
AUDIT=${CONFIG_VALUES[security_audit]}
FIREWALL=${CONFIG_VALUES[firewall]}
SSH_PORT=${CONFIG_VALUES[ssh_port]}
EOF
      ;;
    *)
      echo "Unknown feature: $feature" | tee -a "$LOG_FILE"
      ;;
  esac
done

echo "Configuration complete" | tee -a "$LOG_FILE"
ls -la "$CONFIG_DIR"

## Dry-Run Script
# The following would verify configuration but not apply it
# for feature in "${ENABLED_FEATURES[@]}"; do
#   echo "Would configure $feature with settings from ${CONFIG_DIR}/${feature}.conf"
#   if [ -f "${CONFIG_DIR}/${feature}.conf" ]; then
#     cat "${CONFIG_DIR}/${feature}.conf"
#   else
#     echo "Warning: No configuration file for $feature"
#   fi
# done

```
#### With Dependencies
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# SYSTEM_TYPE="server"
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# CONFIG_DIR=""/mnt/root"/etc/config"
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
SECURITY_LEVEL=${SECURITY_LEVEL:-"high"}
NETWORK_TYPE=${NETWORK_TYPE:-"bridged"}
declare -A CONFIG_VALUES=(
  [security_audit]="yes"
  [firewall]="enabled"
  [ssh_port]="2222"
)
## Script
# Configure enabled features
echo "Configuring features..." | tee -a "$LOG_FILE"

for feature in "${ENABLED_FEATURES[@]}"; do
  case "$feature" in
    networking)
      echo "Setting up $NETWORK_TYPE networking..." | tee -a "$LOG_FILE"
      cat > "${CONFIG_DIR}/network.conf" << EOF
TYPE=$NETWORK_TYPE
DHCP=yes
HOSTNAME=example-${SYSTEM_TYPE}
EOF
      ;;
    security)
      echo "Configuring $SECURITY_LEVEL security..." | tee -a "$LOG_FILE"
      cat > "${CONFIG_DIR}/security.conf" << EOF
LEVEL=$SECURITY_LEVEL
AUDIT=${CONFIG_VALUES[security_audit]}
FIREWALL=${CONFIG_VALUES[firewall]}
SSH_PORT=${CONFIG_VALUES[ssh_port]}
EOF
      ;;
    *)
      echo "Unknown feature: $feature" | tee -a "$LOG_FILE"
      ;;
  esac
done

echo "Configuration complete" | tee -a "$LOG_FILE"
ls -la "$CONFIG_DIR"
## Dry-Run Script
# The following would verify configuration but not apply it
# for feature in "${ENABLED_FEATURES[@]}"; do
#   echo "Would configure $feature with settings from ${CONFIG_DIR}/${feature}.conf"
#   if [ -f "${CONFIG_DIR}/${feature}.conf" ]; then
#     cat "${CONFIG_DIR}/${feature}.conf"
#   else
#     echo "Warning: No configuration file for $feature"
#   fi
# done
```

---


### Block 7
#### Original Block
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# CONFIG_DIR="${MOUNT2}/etc/config"
# SYSTEM_TYPE="server"
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
# Generate a UUID for this installation
UUID=$(cat /proc/sys/kernel/random/uuid)
INSTALL_ID="${SYSTEM_TYPE}-${UUID:0:8}"
ERROR_COUNT=0
WARNINGS=()
MAX_ERRORS=2

error_handler() {
  local msg="$1"
  ERROR_COUNT=$((ERROR_COUNT + 1))
  echo "ERROR[$ERROR_COUNT]: $msg" | tee -a "$LOG_FILE"
  
  if [ "$ERROR_COUNT" -ge "$MAX_ERRORS" ]; then
    echo "Too many errors, aborting" | tee -a "$LOG_FILE"
    exit 1
  fi
}

warn() {
  local msg="$1"
  WARNINGS+=("$msg")
  echo "WARNING: $msg" | tee -a "$LOG_FILE"
}

## Script
echo "Starting system initialization with ID: $INSTALL_ID" | tee -a "$LOG_FILE"

# Check for required files
if [ ! -f "${CONFIG_DIR}/system.conf" ]; then
  error_handler "Missing system configuration file"
fi

# Look for security settings
if [ ! -f "${CONFIG_DIR}/security.conf" ]; then
  warn "No security configuration found, using defaults"
fi

# Create installation record
cat > "${CONFIG_DIR}/installation.json" << EOF
{
  "id": "${INSTALL_ID}",
  "timestamp": "$(date -Iseconds)",
  "system_type": "${SYSTEM_TYPE}",
  "warning_count": ${#WARNINGS[@]},
  "error_count": ${ERROR_COUNT}
}
EOF

echo "Installation record created. Warnings: ${#WARNINGS[@]}" | tee -a "$LOG_FILE"
if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo "Warning details:" | tee -a "$LOG_FILE"
  printf " - %s\n" "${WARNINGS[@]}" | tee -a "$LOG_FILE"
fi

```
#### With Dependencies
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# SYSTEM_TYPE="server"
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# CONFIG_DIR=""/mnt/root"/etc/config"
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
# Generate a UUID for this installation
UUID=$(cat /proc/sys/kernel/random/uuid)
INSTALL_ID="${SYSTEM_TYPE}-${UUID:0:8}"
ERROR_COUNT=0
WARNINGS=()
MAX_ERRORS=2

error_handler() {
  local msg="$1"
  ERROR_COUNT=$((ERROR_COUNT + 1))
  echo "ERROR[$ERROR_COUNT]: $msg" | tee -a "$LOG_FILE"
  
  if [ "$ERROR_COUNT" -ge "$MAX_ERRORS" ]; then
    echo "Too many errors, aborting" | tee -a "$LOG_FILE"
    exit 1
  fi
}

warn() {
  local msg="$1"
  WARNINGS+=("$msg")
  echo "WARNING: $msg" | tee -a "$LOG_FILE"
}
## Script
echo "Starting system initialization with ID: $INSTALL_ID" | tee -a "$LOG_FILE"

# Check for required files
if [ ! -f "${CONFIG_DIR}/system.conf" ]; then
  error_handler "Missing system configuration file"
fi

# Look for security settings
if [ ! -f "${CONFIG_DIR}/security.conf" ]; then
  warn "No security configuration found, using defaults"
fi

# Create installation record
cat > "${CONFIG_DIR}/installation.json" << EOF
{
  "id": "${INSTALL_ID}",
  "timestamp": "$(date -Iseconds)",
  "system_type": "${SYSTEM_TYPE}",
  "warning_count": ${#WARNINGS[@]},
  "error_count": ${ERROR_COUNT}
}
EOF

echo "Installation record created. Warnings: ${#WARNINGS[@]}" | tee -a "$LOG_FILE"
if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo "Warning details:" | tee -a "$LOG_FILE"
  printf " - %s\n" "${WARNINGS[@]}" | tee -a "$LOG_FILE"
fi
```

---


### Block 8
#### Original Block
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# CONFIG_DIR="${MOUNT2}/etc/config"
# INSTALL_ID="server-12345678"
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
SHELLS=("/bin/bash" "/bin/zsh")
DEFAULT_SHELL="/bin/bash"
SHELL_CONFIG_DIR="${MOUNT2}/etc/skel"

generate_shell_config() {
  local shell="$1"
  local shell_name=$(basename "$shell")
  local config_file
  
  case "$shell_name" in
    bash)
      config_file="${SHELL_CONFIG_DIR}/.bashrc"
      ;;
    zsh)
      config_file="${SHELL_CONFIG_DIR}/.zshrc"
      ;;
    *)
      warn "Unsupported shell: $shell_name"
      return 1
      ;;
  esac
  
  echo "Generating config for $shell_name at $config_file" | tee -a "$LOG_FILE"
  
  mkdir -p "$(dirname "$config_file")"
  
  cat > "$config_file" << EOF
# Generated for $shell_name by setup script
# Installation: $INSTALL_ID

# Environment setup
export PATH=\$PATH:/usr/local/bin
export EDITOR=nano

# Aliases
alias ll='ls -la'
alias ..='cd ..'

# System specific
export SYSTEM_TYPE="${SYSTEM_TYPE}"
EOF

  if [ "$shell_name" = "zsh" ]; then
    cat >> "$config_file" << EOF
# ZSH specific settings
autoload -Uz compinit
compinit

# ZSH prompt
PROMPT='%F{green}%n@%m%f:%F{blue}%~%f\$ '
EOF
  fi
  
  return 0
}

## Script
echo "Setting up shell configurations..." | tee -a "$LOG_FILE"

mkdir -p "$SHELL_CONFIG_DIR"

# Generate configs for all supported shells
for shell in "${SHELLS[@]}"; do
  if ! generate_shell_config "$shell"; then
    warn "Failed to generate config for $shell"
  fi
done

# Set default shell
echo "Setting default shell to $DEFAULT_SHELL" | tee -a "$LOG_FILE"
echo "$DEFAULT_SHELL" > "${MOUNT2}/etc/default-shell"

# List the generated config files
find "$SHELL_CONFIG_DIR" -type f -name ".*rc" | sort

```
#### With Dependencies
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# SYSTEM_TYPE="server"
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# INSTALL_ID=""server"-${UUID:0:8}"
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
SHELLS=("/bin/bash" "/bin/zsh")
DEFAULT_SHELL="/bin/bash"
SHELL_CONFIG_DIR="${MOUNT2}/etc/skel"

generate_shell_config() {
  local shell="$1"
  local shell_name=$(basename "$shell")
  local config_file
  
  case "$shell_name" in
    bash)
      config_file="${SHELL_CONFIG_DIR}/.bashrc"
      ;;
    zsh)
      config_file="${SHELL_CONFIG_DIR}/.zshrc"
      ;;
    *)
      warn "Unsupported shell: $shell_name"
      return 1
      ;;
  esac
  
  echo "Generating config for $shell_name at $config_file" | tee -a "$LOG_FILE"
  
  mkdir -p "$(dirname "$config_file")"
  
  cat > "$config_file" << EOF
# Generated for $shell_name by setup script
# Installation: $INSTALL_ID

# Environment setup
export PATH=\$PATH:/usr/local/bin
export EDITOR=nano

# Aliases
alias ll='ls -la'
alias ..='cd ..'

# System specific
export SYSTEM_TYPE="${SYSTEM_TYPE}"
EOF

  if [ "$shell_name" = "zsh" ]; then
    cat >> "$config_file" << EOF
# ZSH specific settings
autoload -Uz compinit
compinit

# ZSH prompt
PROMPT='%F{green}%n@%m%f:%F{blue}%~%f\$ '
EOF
  fi
  
  return 0
}
## Script
echo "Setting up shell configurations..." | tee -a "$LOG_FILE"

mkdir -p "$SHELL_CONFIG_DIR"

# Generate configs for all supported shells
for shell in "${SHELLS[@]}"; do
  if ! generate_shell_config "$shell"; then
    warn "Failed to generate config for $shell"
  fi
done

# Set default shell
echo "Setting default shell to $DEFAULT_SHELL" | tee -a "$LOG_FILE"
echo "$DEFAULT_SHELL" > "${MOUNT2}/etc/default-shell"

# List the generated config files
find "$SHELL_CONFIG_DIR" -type f -name ".*rc" | sort
```

---


### Block 9
#### Original Block
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"

## Variables
APP_USER="appuser"
APP_GROUP="appgroup"
APP_UID=1000
APP_GID=1000
APP_DIR="${MOUNT2}/opt/myapp"
DATA_DIRS=("config" "data" "logs" "cache")
PERMISSIONS=(755 775 770 770)

## Script
echo "Setting up application directories and permissions..." | tee -a "$LOG_FILE"

# Create user and group entries in password and group files
mkdir -p "${MOUNT2}/etc"
echo "${APP_USER}:x:${APP_UID}:${APP_GID}:Application User:/home/${APP_USER}:/bin/bash" >> "${MOUNT2}/etc/passwd"
echo "${APP_GROUP}:x:${APP_GID}:" >> "${MOUNT2}/etc/group"

# Create app directory structure
mkdir -p "$APP_DIR"

# Create data directories with appropriate permissions
for i in "${!DATA_DIRS[@]}"; do
  dir="${APP_DIR}/${DATA_DIRS[$i]}"
  perm="${PERMISSIONS[$i]}"
  
  echo "Creating $dir with permissions $perm" | tee -a "$LOG_FILE"
  mkdir -p "$dir"
  chmod "$perm" "$dir"
  chown "${APP_UID}:${APP_GID}" "$dir"
done

# Create a simple app configuration
cat > "${APP_DIR}/config/app.conf" << EOF
# Application Configuration
app_name = My Application
version = 1.0.0
log_level = info
data_path = ${APP_DIR}/data
cache_path = ${APP_DIR}/cache
log_path = ${APP_DIR}/logs
EOF

# Set proper ownership for configuration
chown "${APP_UID}:${APP_GID}" "${APP_DIR}/config/app.conf"
chmod 640 "${APP_DIR}/config/app.conf"

# Show directory structure and permissions
find "$APP_DIR" -type d | sort | xargs ls -ld

## Dry-Run Script
# echo "Would create the following directory structure:"
# for i in "${!DATA_DIRS[@]}"; do
#   echo "${APP_DIR}/${DATA_DIRS[$i]} (${PERMISSIONS[$i]})"
# done
# 
# echo "Would create user ${APP_USER} with UID ${APP_UID}"
# echo "Would create group ${APP_GROUP} with GID ${APP_GID}"

```
#### With Dependencies
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
APP_USER="appuser"
APP_GROUP="appgroup"
APP_UID=1000
APP_GID=1000
APP_DIR="${MOUNT2}/opt/myapp"
DATA_DIRS=("config" "data" "logs" "cache")
PERMISSIONS=(755 775 770 770)
## Script
echo "Setting up application directories and permissions..." | tee -a "$LOG_FILE"

# Create user and group entries in password and group files
mkdir -p "${MOUNT2}/etc"
echo "${APP_USER}:x:${APP_UID}:${APP_GID}:Application User:/home/${APP_USER}:/bin/bash" >> "${MOUNT2}/etc/passwd"
echo "${APP_GROUP}:x:${APP_GID}:" >> "${MOUNT2}/etc/group"

# Create app directory structure
mkdir -p "$APP_DIR"

# Create data directories with appropriate permissions
for i in "${!DATA_DIRS[@]}"; do
  dir="${APP_DIR}/${DATA_DIRS[$i]}"
  perm="${PERMISSIONS[$i]}"
  
  echo "Creating $dir with permissions $perm" | tee -a "$LOG_FILE"
  mkdir -p "$dir"
  chmod "$perm" "$dir"
  chown "${APP_UID}:${APP_GID}" "$dir"
done

# Create a simple app configuration
cat > "${APP_DIR}/config/app.conf" << EOF
# Application Configuration
app_name = My Application
version = 1.0.0
log_level = info
data_path = ${APP_DIR}/data
cache_path = ${APP_DIR}/cache
log_path = ${APP_DIR}/logs
EOF

# Set proper ownership for configuration
chown "${APP_UID}:${APP_GID}" "${APP_DIR}/config/app.conf"
chmod 640 "${APP_DIR}/config/app.conf"

# Show directory structure and permissions
find "$APP_DIR" -type d | sort | xargs ls -ld
## Dry-Run Script
# echo "Would create the following directory structure:"
# for i in "${!DATA_DIRS[@]}"; do
#   echo "${APP_DIR}/${DATA_DIRS[$i]} (${PERMISSIONS[$i]})"
# done
# 
# echo "Would create user ${APP_USER} with UID ${APP_UID}"
# echo "Would create group ${APP_GROUP} with GID ${APP_GID}"
```

---


### Block 10
#### Original Block
```bash

## Preset Variables
# MOUNT1="/mnt/boot"
# MOUNT2="/mnt/root"
# CONFIG_DIR="${MOUNT2}/etc/config"
# APP_DIR="${MOUNT2}/opt/myapp"
# LOG_FILE="/tmp/disk_setup_${TIMESTAMP}.log"
# INSTALL_ID="server-12345678"

## Variables
SUMMARY_FILE="${MOUNT2}/installation_summary.txt"
CHECK_COMMANDS=(
  "ls -la ${MOUNT1}"
  "ls -la ${MOUNT2}/etc"
  "find ${CONFIG_DIR} -type f | sort"
  "ls -la ${APP_DIR}"
)
SUCCESS_CRITERIA=(
  "${CONFIG_DIR}/system.conf"
  "${CONFIG_DIR}/security.conf"
  "${CONFIG_DIR}/installation.json"
  "${APP_DIR}/config/app.conf"
)

## Script
echo "Performing final validation..." | tee -a "$LOG_FILE"

# Run check commands and collect outputs
echo "=== Installation Summary ($INSTALL_ID) ===" > "$SUMMARY_FILE"
echo "Generated on: $(date)" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# Check for critical files
echo "=== Critical Files ===" >> "$SUMMARY_FILE"
all_present=true
for file in "${SUCCESS_CRITERIA[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ Found: $file" >> "$SUMMARY_FILE"
  else
    echo "✗ Missing: $file" >> "$SUMMARY_FILE"
    all_present=false
  fi
done

echo "" >> "$SUMMARY_FILE"
echo "=== Filesystem Structure ===" >> "$SUMMARY_FILE"

# Run and capture outputs of check commands
for cmd in "${CHECK_COMMANDS[@]}"; do
  echo "" >> "$SUMMARY_FILE"
  echo "$ $cmd" >> "$SUMMARY_FILE"
  eval "$cmd" >> "$SUMMARY_FILE" 2>&1
done

# Final status
echo "" >> "$SUMMARY_FILE"
echo "=== Final Status ===" >> "$SUMMARY_FILE"
if [ "$all_present" = true ]; then
  echo "Installation SUCCESSFUL" >> "$SUMMARY_FILE"
  echo "All required files are present" >> "$SUMMARY_FILE"
else
  echo "Installation INCOMPLETE" >> "$SUMMARY_FILE"
  echo "Some required files are missing" >> "$SUMMARY_FILE"
fi

echo "Summary file created at $SUMMARY_FILE" | tee -a "$LOG_FILE"
cat "$SUMMARY_FILE" | tee -a "$LOG_FILE"

```
#### With Dependencies
```bash

## Preset Variables
# MOUNT2="/mnt/root"
# MOUNT1="/mnt/boot"
# APP_DIR=""/mnt/root"/opt/myapp"
# LOG_FILE="/tmp/disk_setup_$(date +%Y%m%d_%H%M%S).log"
# CONFIG_DIR=""/mnt/root"/etc/config"
# INSTALL_ID=""server"-${UUID:0:8}"
# TIMESTAMP=$(date +%Y%m%d_%H%M%S)

## Variables
SUMMARY_FILE="${MOUNT2}/installation_summary.txt"
CHECK_COMMANDS=(
  "ls -la ${MOUNT1}"
  "ls -la ${MOUNT2}/etc"
  "find ${CONFIG_DIR} -type f | sort"
  "ls -la ${APP_DIR}"
)
SUCCESS_CRITERIA=(
  "${CONFIG_DIR}/system.conf"
  "${CONFIG_DIR}/security.conf"
  "${CONFIG_DIR}/installation.json"
  "${APP_DIR}/config/app.conf"
)
## Script
echo "Performing final validation..." | tee -a "$LOG_FILE"

# Run check commands and collect outputs
echo "=== Installation Summary ($INSTALL_ID) ===" > "$SUMMARY_FILE"
echo "Generated on: $(date)" >> "$SUMMARY_FILE"
echo "" >> "$SUMMARY_FILE"

# Check for critical files
echo "=== Critical Files ===" >> "$SUMMARY_FILE"
all_present=true
for file in "${SUCCESS_CRITERIA[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ Found: $file" >> "$SUMMARY_FILE"
  else
    echo "✗ Missing: $file" >> "$SUMMARY_FILE"
    all_present=false
  fi
done

echo "" >> "$SUMMARY_FILE"
echo "=== Filesystem Structure ===" >> "$SUMMARY_FILE"

# Run and capture outputs of check commands
for cmd in "${CHECK_COMMANDS[@]}"; do
  echo "" >> "$SUMMARY_FILE"
  echo "$ $cmd" >> "$SUMMARY_FILE"
  eval "$cmd" >> "$SUMMARY_FILE" 2>&1
done

# Final status
echo "" >> "$SUMMARY_FILE"
echo "=== Final Status ===" >> "$SUMMARY_FILE"
if [ "$all_present" = true ]; then
  echo "Installation SUCCESSFUL" >> "$SUMMARY_FILE"
  echo "All required files are present" >> "$SUMMARY_FILE"
else
  echo "Installation INCOMPLETE" >> "$SUMMARY_FILE"
  echo "Some required files are missing" >> "$SUMMARY_FILE"
fi

echo "Summary file created at $SUMMARY_FILE" | tee -a "$LOG_FILE"
cat "$SUMMARY_FILE" | tee -a "$LOG_FILE"
```

---


**Total blocks: 10**

---

