# Sasquatch Universal Builder (RC 1)
**Developed by: M-Tarantino**

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20(Android)-green.svg)](#)

## 📌 Overview
**Sasquatch** is the industry-standard tool for extracting non-standard SquashFS images, which are frequently encountered during embedded firmware analysis. However, the original project (by devttys0) has been unmaintained for years, causing it to fail on modern compilers (GCC 10+) due to stricter linker rules (e.g., `duplicate symbol: verbose`).

The **Sasquatch Universal Builder** is a modern orchestration script designed to bridge this gap. It automates the entire process of fetching, patching, and compiling Sasquatch, ensuring it works flawlessly on today's systems—including mobile environments like **Termux**.

## ✨ Key Features
* **On-the-fly Refactoring:** Dynamically patches legacy C-headers using regex to resolve `extern` variable conflicts.
* **Smart Environment Detection:** Automatically identifies the OS (Debian/Ubuntu, Arch, Fedora, Alpine, or Termux) and handles dependency installation.
* **Binary-Safe Patching:** Uses `latin-1` encoding to handle legacy source files and patches without corruption.
* **Termux Optimized:** Tailored to work within the Android/Termux environment, turning your phone into a mobile firmware analysis station.
* **Legacy Compliance:** Automatically enforces `-fcommon` flags where necessary.

## 🚀 Installation & Usage

### 1. Prerequisites
You only need `python3` and `wget` installed. The builder will handle the rest.

### 2. Execution
Download the builder script and run it:

    wget https://raw.githubusercontent.com/M-Tarantino/Sasquatch-Universal-Builder/main/SASQUATCH_UNIVERSAL_BUILDER.py
    python3 SASQUATCH_UNIVERSAL_BUILDER.py

### 3. Usage
Once the build is successful, run Sasquatch as follows:

    sasquatch [options] filesystem.squashfs

## 🛠 Technical Background (The "Why")
This project was born out of the necessity to keep vital security tools alive. The main challenge with the original Sasquatch was the way global variables were declared in multiple `.c` files. Modern compilers default to `-fno-common`, which treats these as duplicate symbols.

Instead of providing a static, pre-patched source, this builder **analyzes the source code during the build process** and applies the necessary C-level modifications automatically.

## 🤝 Credits & Acknowledgments
* **Original Logic:** Craig Heffner ([@devttys0](https://github.com/devttys0)).
* **SquashFS Foundation:** Phillip Lougher for the original implementation.
* **Engineering & Automation:** Developed and maintained by **M-Tarantino**.

## ⚖️ License
This script is licensed under the **GNU General Public License v2.0**.
* The underlying SquashFS code and patches remain under their respective GPLv2 licenses.

---
*Note: This project was developed using an AI-assisted engineering workflow to solve legacy build issues in record time.*
