# 🛠️ Sasquatch Universal Builder
**A Memory-Safe Automation Script for Compiling Sasquatch on Modern Systems & Termux.**

[![Language](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Android%20(Termux)%20%7C%20ARM64-green.svg)](https://github.com/termux/termux-app)
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
3.  **Dynamic Patching:** Fixes legacy C-headers on-the-fly using regex.
4.  **Zero Manual Configuration:** It just works.
5.  **Multi-Platform CI/CD:** Automated testing on 10+ distributions (x86_64 & ARM64) via GitHub Actions.
6.  **SSL Resilience:** Handles SSL certificate issues in containers with automatic fallback to HTTP.

---

### 📋 Prerequisites & Automation
The builder is designed to be as "hands-off" as possible. 
* **Requirements:** You only need `python3` installed.
* **Automation:** The script detects your OS and installs all build-essential tools and libraries.
* **Note:** On Linux systems, the script will request `sudo` access to install dependencies. On **Termux**, it runs natively without root.

---

### ⚠️ Status & Compatibility
* **XZ Compression:** This version focuses on maximum compatibility across legacy and modern GCC versions. Therefore, XZ-compressed SquashFS support is currently disabled.
* **Supported Architectures:**
  - ✅ x86_64 (Standard Linux Servers & Desktops)
  - ✅ ARM64 (Raspberry Pi, IoT Devices, ARM-based Cloud Instances)

---

### 🚀 Installation & Usage

#### Basic Usage
```bash
git clone [https://github.com/M-Tarantino/Sasquatch-Universal-Builder.git](https://github.com/M-Tarantino/Sasquatch-Universal-Builder.git)
cd Sasquatch-Universal-Builder
python3 SASQUATCH_UNIVERSAL_BUILDER.py
