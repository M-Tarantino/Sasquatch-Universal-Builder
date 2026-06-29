# 🛠️ Sasquatch Universal Builder
**A Memory-Safe Automation Script for Compiling Sasquatch on Modern Systems & Termux.**

[![Language](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Android%20(Termux)-green.svg)](https://github.com/termux/termux-app)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue.svg)](https://github.com/M-Tarantino/Sasquatch-Universal-Builder/actions)

---

### 📖 The Problem
`Sasquatch` (by @devttys0) is the industry-standard tool for extracting non-standard SquashFS images. However, the original code hasn't been updated in years, causing it to fail on modern compilers (GCC 10+) due to:
- Stricter linker rules (e.g., `duplicate symbol: verbose`)
- Incompatible signal handler signatures (POSIX compliance)
- Missing LZO header includes on Alpine/musl systems
- Legacy C-code not conforming to modern standards

### 💡 The Solution: Pure Automation
The **Sasquatch Universal Builder** is designed to be a "run-and-forget" solution. Unlike other forks, this is a modern orchestrator that:
1.  **Smart Environment Detection:** Identifies your OS and package manager (apt, pacman, dnf, apk, pkg).
2.  **Auto-Dependency Install:** Automatically installs `gcc`, `make`, `zlib`, `lzma`, `lzo`, `curl`, etc.
3.  **Dynamic Patching:** Fixes legacy C-headers on-the-fly using regex:
    - Resolves `extern` variable conflicts
    - Fixes signal handler signatures for POSIX compliance
    - Injects compatibility headers for musl/Alpine systems
    - Handles LZO include path variations
4.  **Zero Manual Configuration:** It just works.
5.  **Multi-Platform CI/CD:** Automated testing on Debian, Alpine, Arch Linux, and Fedora via GitHub Actions.
6.  **SSL Resilience:** Handles SSL certificate issues in containers with automatic fallback to HTTP.

---

### 📋 Prerequisites & Automation
The builder is designed to be as "hands-off" as possible. 
* **Requirements:** You only need `python3` installed.
* **Automation:** The script detects your OS and installs all build-essential tools and libraries.
* **Note:** On Linux systems, the script will request `sudo` access to install dependencies (auto-detected). On **Termux**, it runs natively without root.

---

### ⚠️ Current Limitations & Status
* **XZ Compression:** This version focuses on maximum compatibility across legacy and modern GCC versions. Therefore, XZ-compressed SquashFS support is currently disabled.
* **Supported Platforms:** Optimized and tested for:
  - ✅ Debian/Ubuntu (Bullseye+)
  - ✅ Alpine Linux (musl-based)
  - ✅ Arch Linux
  - ✅ Fedora/RHEL
  - ✅ Termux (Android)

---

### 🚀 Installation & Usage

#### Basic Usage
```bash
git clone https://github.com/M-Tarantino/Sasquatch-Universal-Builder.git
cd Sasquatch-Universal-Builder
python3 SASQUATCH_UNIVERSAL_BUILDER.py
```

#### Verbose Mode (Debug)
For detailed compilation output and troubleshooting:
```bash
python3 SASQUATCH_UNIVERSAL_BUILDER.py --verbose
# or
python3 SASQUATCH_UNIVERSAL_BUILDER.py -v
```

#### Verify Installation
```bash
sasquatch -h
# or
which sasquatch
```

---

### 🔧 Technical Details

#### Automatic Fixes Applied
This builder doesn't just copy files. It **analyzes and patches the source code**:

1. **Signal Handler Compliance (POSIX)**
   - Converts `void handler()` → `void handler(int sig)`
   - Fixes incompatible pointer type errors

2. **Symbol Resolution**
   - Uses regex to convert `int verbose = 0;` → `extern int verbose;` in headers
   - Injects global definition in unsquashfs.c

3. **Compatibility Header Injection**
   - Creates `compat.h` for musl-based systems
   - Defines missing symbols (FNM_EXTMATCH, S_IFBLK, S_IFCHR)
   - Auto-injects into source files

4. **LZO Header Path Normalization**
   - Handles variant include paths across distros
   - Provides fallback includes for compatibility

5. **Compiler Flag Optimization**
   - Removes `-Werror` for legacy code
   - Adds `-fcommon` for GCC 10+ compatibility
   - Configures CFLAGS/LIBS per platform

6. **Network Resilience**
   - Automatic wget → curl fallback for downloads
   - Disables SSL verification in containers (auto-detected)
   - HTTP fallback for git operations

#### Environment Detection Logic
```
Linux System Detected
├── apt-get → Debian/Ubuntu
├── pacman → Arch Linux
├── dnf → Fedora/RHEL
├── apk → Alpine Linux
└── pkg → Termux (Android)
```

---

### 🛠️ Development & CI/CD

#### GitHub Actions Matrix
The project includes automated multi-platform builds:
- **Debian (trixie)** - APT package manager
- **Alpine (latest)** - APK package manager (musl libc)
- **Arch Linux (latest)** - Pacman package manager
- **Fedora (latest)** - DNF package manager

View test results: [GitHub Actions](https://github.com/M-Tarantino/Sasquatch-Universal-Builder/actions)

#### Local Testing (Docker)
```bash
# Test on Debian
docker run --rm -v $(pwd):/work -w /work debian:latest \
  bash -c "apt-get update && python3 /work/SASQUATCH_UNIVERSAL_BUILDER.py -v"

# Test on Alpine
docker run --rm -v $(pwd):/work -w /work alpine:latest \
  sh -c "apk add --no-cache python3 && python3 /work/SASQUATCH_UNIVERSAL_BUILDER.py -v"
```

---

### 🤝 Credits & Acknowledgments
* **Original Tool:** [Sasquatch](https://github.com/devttys0/sasquatch) by **Craig Heffner** (@devttys0).
* **Modern Automation & Fixes:** Developed by **James Tarantino** (@M-Tarantino).

---

### 👤 Author
**Muneeb Tarantino**
* **GitHub:** [@M-Tarantino](https://github.com/M-Tarantino)
* **Contact:** muneeb.tarantino.job@gmail.com

---

### 📝 License
GNU General Public License v2 (GPLv2) - See LICENSE file for details.

---

*Note: This project was developed using an AI-assisted engineering workflow to solve legacy build issues across multiple platforms in record time.*
