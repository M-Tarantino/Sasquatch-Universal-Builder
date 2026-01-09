# 🛠️ Sasquatch Universal Builder
**A Memory-Safe Automation Script for Compiling Sasquatch on Modern Systems & Termux.**

[![Language](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Android%20(Termux)-green.svg)](https://github.com/termux/termux-app)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

---

### 📖 The Problem
`Sasquatch` (by @devttys0) is the industry-standard tool for extracting non-standard SquashFS images during firmware analysis. However, the original source code hasn't been updated in years, causing it to fail on modern compilers (GCC 10+) due to stricter linker rules (e.g., `duplicate symbol: verbose`).

### 💡 The Solution
The **Sasquatch Universal Builder** is a modern orchestration script that:
1.  **Automates** the entire environment setup and dependency handling.
2.  **Fetches** the original source code dynamically from the source.
3.  **Patches** legacy C-headers on-the-fly using regex to resolve `extern` variable conflicts.
4.  **Compiles** and installs the tool safely, even on Android/Termux environments.

---

### 📋 Smart Dependency Management
The builder is fully automated. When you run the script, it detects your OS and package manager to install the required tools for you. It supports:
* **Package Managers:** `apt` (Debian/Ubuntu), `pkg` (Termux), `pacman` (Arch), `dnf` (Fedora), and `apk` (Alpine).
* **Automated Install of:** `gcc`/`clang`, `make`, `patch`, `zlib`, `lzma`, `lzo`, and `git`.

*Note: On Linux, the script will request `sudo` to handle the installation. On Termux, it runs natively.*

---

### 🚀 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/M-Tarantino/Sasquatch-Universal-Builder.git](https://github.com/M-Tarantino/Sasquatch-Universal-Builder.git)
    cd Sasquatch-Universal-Builder
    ```

2.  **Run the automated builder:**
    ```bash
    python3 SASQUATCH_UNIVERSAL_BUILDER.py
    ```

3.  **Verify the installation:**
    Simply type `sasquatch -h` in your terminal.

---

### 🛠️ Technical Background
Instead of providing a static, pre-patched source, this builder **analyzes the source code during the build process**. 
* **Dynamic Refactoring:** Uses Python's `re.sub` with `latin-1` encoding to handle legacy files without corruption.
* **Compiler Flags:** Automatically enforces `-fcommon` flags where necessary to bridge the gap between GCC versions.
* **Mobile Ready:** Specifically optimized for the unique environment of Termux (Android).

---

### 🤝 Credits & Acknowledgments
* **Original Tool:** [Sasquatch](https://github.com/devttys0/sasquatch) by **Craig Heffner** (@devttys0).
* **Engineering & Automation:** Developed by **Muneeb Tarantino**.

---

### 👤 Author
**Muneeb Tarantino**
* **LinkedIn:** [muneeb-tarantino](https://www.linkedin.com/in/muneeb-tarantino/)
* **GitHub:** [@M-Tarantino](https://github.com/M-Tarantino)

---
*Note: This project was developed using an AI-assisted engineering workflow to solve legacy build issues in record time.*
