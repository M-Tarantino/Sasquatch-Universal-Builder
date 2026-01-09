# 🛠️ Sasquatch Universal Builder
**A Memory-Safe Automation Script for Compiling Sasquatch on Modern Systems & Termux.**

[![Language](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Android%20(Termux)-green.svg)](https://github.com/termux/termux-app)
[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

---

### 📖 The Problem
`Sasquatch` (by @devttys0) is the industry-standard tool for extracting non-standard SquashFS images. However, the original code hasn't been updated in years, causing it to fail on modern compilers (GCC 10+) due to stricter linker rules (e.g., `duplicate symbol: verbose`).

### 💡 The Solution: Pure Automation
The **Sasquatch Universal Builder** is designed to be a "run-and-forget" solution. Unlike other forks, this is a modern orchestrator that:
1.  **Smart Environment Detection:** Identifies your OS and package manager.
2.  **Auto-Dependency Install:** Automatically installs `gcc`, `make`, `zlib`, `lzma`, etc.
3.  **Dynamic Patching:** Fixes legacy C-headers on-the-fly using regex.
4.  **Zero Manual Configuration:** It just works.


---

### 📋 Prerequisites & Automation
The builder is designed to be as "hands-off" as possible. 
* **Requirements:** You only need `python3` and `git` installed.
* **Automation:** The script detects your OS and installs all build-essential tools and libraries.
* **Note:** On Linux systems, the script will request `sudo` access to install these dependencies. On **Termux**, it runs natively without root.

---

### ⚠️ Current Limitations
* **XZ Compression:** This version focuses on maximum compatibility across legacy and modern GCC versions. Therefore, XZ-compressed SquashFS support is currently disabled.
* **Environment:** Optimized and tested for Ubuntu 20.04+, Arch Linux, and Termux.

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
This builder doesn't just copy files. It **analyzes the source code during the build process**:
* **Regex Refactoring:** Uses Python's `re.sub` to resolve `extern` variable conflicts dynamically.
* **Compiler Bridge:** Automatically enforces `-fcommon` flags to bridge the gap between GCC versions.
* **Mobile First:** Specifically optimized for the unique environment of **Termux (Android)**.

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
