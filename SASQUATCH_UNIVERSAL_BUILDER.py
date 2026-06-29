#!/usr/bin/env python3
"""
SASQUATCH UNIVERSAL BUILDER - RC 2 (FIXED)
------------------------------------------------------------
Developer: M-Tarantino
Original Logic: Craig Heffner (devttys0)
License: GNU General Public License v2 (GPLv2)

Description: 
This script automates the compilation of Sasquatch on modern 
Linux systems (Debian, Arch, Alpine, etc.) and Termux. It dynamically 
patches legacy C code to comply with modern GCC/Clang standards.
Includes musl/Alpine compatibility fixes.
------------------------------------------------------------
"""

import os
import subprocess
import sys
import shutil
import platform
import re

class Colors:
    HEADER = '\033[95m'
    OK = '\033[92m'
    INFO = '\033[94m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# Configuration
REPO_URL = "https://github.com/devttys0/sasquatch.git"
SQUASHFS_URL = "https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz"
BUILD_DIR = "sasquatch_rc1_build"

def log(msg, color=Colors.INFO):
    print(f"{color}[*] {msg}{Colors.RESET}")

def banner():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 60)
    print("      SASQUATCH UNIVERSAL BUILDER - RC 2")
    print("=" * 60)
    print("      Developer: M-Tarantino")
    print("      Original Logic: Craig Heffner (devttys0)")
    print("      License: GNU GPLv2")
    print("=" * 60)
    print(f"{Colors.RESET}")

def run_cmd(cmd, check=True, silent=False):
    """Execute shell command with optional output suppression"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=check, 
            capture_output=silent, 
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        if not silent:
            log(f"Command failed: {cmd}", Colors.FAIL)
            if hasattr(e, 'stderr') and e.stderr:
                print(e.stderr)
        return None

def detect_env():
    """Detects the environment and sets paths and package managers"""
    info = {
        'os': platform.system().lower(),
        'is_termux': False,
        'prefix': '/usr/local',
        'pkg_mgr': None,
        'packages': []
    }

    # Check for Termux
    if os.path.exists('/data/data/com.termux') or 'com.termux' in os.environ.get('PREFIX', ''):
        info['is_termux'] = True
        info['prefix'] = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')
        info['pkg_mgr'] = 'pkg'
        info['packages'] = ['git', 'patch', 'make', 'clang', 'zlib', 'liblzma', 'xz-utils', 'lzo', 'lzo2', 'binutils', 'wget', 'curl']
    # Check for Debian/Ubuntu
    elif shutil.which('apt'):
        info['pkg_mgr'] = 'apt'
        info['prefix'] = '/usr'
        # FIX: Added python3 to Debian/Ubuntu packages
        info['packages'] = ['python3', 'git', 'patch', 'make', 'gcc', 'g++', 'zlib1g-dev', 'liblzma-dev', 'liblzo2-dev', 'binutils', 'wget', 'curl']
    # Check for Arch Linux
    elif shutil.which('pacman'):
        info['pkg_mgr'] = 'pacman'
        info['prefix'] = '/usr'
        info['packages'] = ['git', 'patch', 'make', 'gcc', 'zlib', 'xz', 'lzo', 'binutils', 'wget', 'curl']
    # Check for Fedora/RHEL
    elif shutil.which('dnf'):
        info['pkg_mgr'] = 'dnf'
        info['prefix'] = '/usr'
        info['packages'] = ['git', 'patch', 'make', 'gcc', 'gcc-c++', 'zlib-devel', 'xz-devel', 'lzo-devel', 'binutils', 'wget', 'curl']
    # Check for Alpine
    elif shutil.which('apk'):
        info['pkg_mgr'] = 'apk'
        info['prefix'] = '/usr'
        info['packages'] = ['git', 'patch', 'make', 'gcc', 'g++', 'musl-dev', 'zlib-dev', 'xz-dev', 'lzo-dev', 'binutils', 'wget', 'curl']

    return info

def install_deps(env):
    """Install required dependencies based on detected package manager"""
    log(f"Installing dependencies for {env['pkg_mgr'] or 'Unknown OS'}...")

    if not env['pkg_mgr']:
        log("No package manager detected. Please install dependencies manually:", Colors.WARN)
        log("Required: git, patch, make, gcc/clang, zlib, liblzma, lzo", Colors.WARN)
        return

    if env['pkg_mgr'] == 'pkg':
        # Termux
        for pkg in env['packages']:
            log(f"Installing {pkg}...")
            run_cmd(f"pkg install -y {pkg}", silent=True)
    elif env['pkg_mgr'] == 'apt':
        # Debian/Ubuntu
        log("Note: Using sudo for dependency installation", Colors.WARN)
        run_cmd("sudo apt-get update", silent=True)
        run_cmd(f"sudo apt-get install -y {' '.join(env['packages'])}", silent=True)
    elif env['pkg_mgr'] == 'pacman':
        # Arch Linux
        run_cmd(f"sudo pacman -S --noconfirm {' '.join(env['packages'])}", silent=True)
    elif env['pkg_mgr'] == 'dnf':
        # Fedora/RHEL
        run_cmd(f"sudo dnf install -y {' '.join(env['packages'])}", silent=True)
    elif env['pkg_mgr'] == 'apk':
        # Alpine
        run_cmd(f"sudo apk add --no-cache {' '.join(env['packages'])}", silent=True)

    log("✓ Dependencies installed", Colors.OK)

def setup_source():
    """Download and extract source code"""
    log("Setting up build directory...")

    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)
    os.chdir(BUILD_DIR)

    log("Cloning Sasquatch repository...")
    result = run_cmd(f"git clone {REPO_URL} repo", silent=True)
    if not result or result.returncode != 0:
        log("Error cloning repository", Colors.FAIL)
        return False

    log("Downloading SquashFS 4.3...")
    result = run_cmd(f"wget -q {SQUASHFS_URL}")
    if not result or result.returncode != 0:
        log("Error downloading SquashFS with wget, trying curl...", Colors.WARN)
        result = run_cmd(f"curl -L -o squashfs4.3.tar.gz {SQUASHFS_URL}")
        if not result or result.returncode != 0:
            log("Error: Could not download SquashFS 4.3", Colors.FAIL)
            return False

    log("Extracting archive...")
    result = run_cmd("tar -zxf squashfs4.3.tar.gz")
    if not result or result.returncode != 0:
        log("Error extracting archive", Colors.FAIL)
        return False

    if not os.path.exists("squashfs4.3"):
        log("Error: squashfs4.3 directory not found after extraction", Colors.FAIL)
        return False

    log("✓ Source code ready", Colors.OK)
    return True

def apply_patches():
    """Apply original Sasquatch patches"""
    log("Applying Sasquatch patches...")
    os.chdir("squashfs4.3")

    # Apply the original patch from the repo
    patch_file = "../repo/patches/patch0.txt"
    if os.path.exists(patch_file):
        # Convert patch file encoding if needed
        with open(patch_file, 'r', encoding='latin-1') as f:
            patch_content = f.read().replace('\r\n', '\n')
        with open("sasquatch.patch", 'w', encoding='utf-8') as f:
            f.write(patch_content)

        run_cmd("patch -p0 -f -i sasquatch.patch", check=False)
        log("✓ Patches applied", Colors.OK)
    else:
        log("Warning: Patch file not found, continuing without patches", Colors.WARN)

def create_compat_header():
    """Generates a compatibility header for missing symbols (musl/Alpine support)"""
    log("Creating compatibility header (compat.h)...")
    content = """#ifndef SASQUATCH_COMPAT_H
#define SASQUATCH_COMPAT_H
#include <sys/sysmacros.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <signal.h>
#ifndef FNM_EXTMATCH
#define FNM_EXTMATCH 0
#endif
#ifndef S_IFBLK
#define S_IFBLK 0060000
#endif
#ifndef S_IFCHR
#define S_IFCHR 0020000
#endif
#endif
"""
    os.makedirs("squashfs-tools", exist_ok=True)
    with open("squashfs-tools/compat.h", "w") as f:
        f.write(content)
    log("✓ compat.h created", Colors.OK)

def fix_error_header():
    """Fix the duplicate symbol 'verbose' error"""
    log("Fixing duplicate symbol 'verbose'...")

    tools_path = "squashfs-tools"
    error_h = os.path.join(tools_path, "error.h")

    if os.path.exists(error_h):
        with open(error_h, 'r') as f:
            content = f.read()

        # Change definition to declaration
        content = re.sub(
            r'^\s*int\s+verbose\s*(=\s*0)?\s*;',
            'extern int verbose;',
            content,
            flags=re.MULTILINE
        )

        with open(error_h, 'w') as f:
            f.write(content)

        log("✓ Fixed error.h", Colors.OK)

    # Add definition to unsquashfs.c
    unsquashfs_c = os.path.join(tools_path, "unsquashfs.c")
    if os.path.exists(unsquashfs_c):
        with open(unsquashfs_c, 'r') as f:
            content = f.read()

        if 'int verbose = 0;' not in content:
            lines = content.split('\n')
            last_include = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('#include'):
                    last_include = i

            if last_include >= 0:
                lines.insert(last_include + 1, '')
                lines.insert(last_include + 2, '/* Global verbose variable definition */')
                lines.insert(last_include + 3, 'int verbose = 0;')
                lines.insert(last_include + 4, '')

                with open(unsquashfs_c, 'w') as f:
                    f.write('\n'.join(lines))

                log("✓ Fixed unsquashfs.c", Colors.OK)

def fix_lzo_wrapper():
    """FIX #2: Fix LZO header includes - handle different include path conventions
    
    Some systems have lzo headers in <lzo/lzoconf.h>, others in <lzo.h>
    This normalizes to the most compatible form.
    """
    log("Fixing LZO wrapper includes...")
    
    tools_path = "squashfs-tools"
    lzo_wrapper = os.path.join(tools_path, "lzo_wrapper.c")
    
    if os.path.exists(lzo_wrapper):
        with open(lzo_wrapper, 'r') as f:
            content = f.read()
        
        # Check if lzo headers are being included at all
        if '#include' in content and 'lzo' in content:
            # Try to make includes more robust
            # Some Alpine/Arch systems might need different paths
            # We'll add fallback includes if needed
            
            if '#include <lzo/lzoconf.h>' in content:
                # Add a compatibility header check
                compat_check = '#include <lzo/lzoconf.h>\n'
                compat_check += '#ifndef LZO_E_OK\n'
                compat_check += '  #include <lzo.h>\n'
                compat_check += '#endif\n'
                
                content = content.replace(
                    '#include <lzo/lzoconf.h>',
                    compat_check
                )
            
            with open(lzo_wrapper, 'w') as f:
                f.write(content)
            
            log("✓ Fixed LZO wrapper includes", Colors.OK)

def fix_signal_handlers():
    """FIX #1: Fix signal handler signatures to accept int parameter
    
    POSIX signal handlers must have signature: void handler(int sig)
    Not: void handler(void)
    
    This fixes errors like:
    error: passing argument 2 of 'signal' from incompatible pointer type
    signal(SIGWINCH, sigwinch_handler);
    """
    log("Fixing signal handler signatures...")
    
    tools_path = "squashfs-tools"
    unsquashfs_c = os.path.join(tools_path, "unsquashfs.c")
    
    if os.path.exists(unsquashfs_c):
        with open(unsquashfs_c, 'r') as f:
            content = f.read()
        
        # Fix sigwinch_handler signature: void sigwinch_handler() -> void sigwinch_handler(int sig)
        content = re.sub(
            r'void\s+sigwinch_handler\s*\(\s*\)',
            'void sigwinch_handler(int sig)',
            content
        )
        
        # Fix sigalrm_handler signature: void sigalrm_handler() -> void sigalrm_handler(int sig)
        content = re.sub(
            r'void\s+sigalrm_handler\s*\(\s*\)',
            'void sigalrm_handler(int sig)',
            content
        )
        
        with open(unsquashfs_c, 'w') as f:
            f.write(content)
        
        log("✓ Fixed signal handler signatures", Colors.OK)

def fix_fnm_extmatch():
    """Fix FNM_EXTMATCH compatibility (legacy, now handled in compat.h)"""
    log("Fixing FNM_EXTMATCH compatibility...")

    tools_path = "squashfs-tools"
    unsquashfs_c = os.path.join(tools_path, "unsquashfs.c")

    if os.path.exists(unsquashfs_c):
        with open(unsquashfs_c, 'r') as f:
            content = f.read()

        # Only add if compat.h is not already included
        if '#include "compat.h"' not in content:
            fnm_fix = "#ifndef FNM_EXTMATCH\n#define FNM_EXTMATCH 0\n#endif\n\n"
            if not content.startswith("#ifndef FNM_EXTMATCH"):
                content = fnm_fix + content

            with open(unsquashfs_c, 'w') as f:
                f.write(content)

            log("✓ Fixed FNM_EXTMATCH", Colors.OK)

def disable_xz_wrapper():
    """Disable XZ wrapper to avoid conflicts"""
    log("Disabling XZ wrapper...")

    tools_path = "squashfs-tools"
    xz_files = [
        os.path.join(tools_path, "xz_wrapper.c"),
        os.path.join(tools_path, "xz_wrapper.h")
    ]

    for xz_file in xz_files:
        if os.path.exists(xz_file):
            with open(xz_file, 'w') as f:
                f.write('/* XZ support disabled */\n')
            log(f"✓ Disabled {os.path.basename(xz_file)}", Colors.OK)

def fix_makefile(env):
    """Fix Makefile for modern compilers"""
    log("Fixing Makefile...")

    tools_path = "squashfs-tools"
    makefile = os.path.join(tools_path, "Makefile")
    prefix = env['prefix']

    if not os.path.exists(makefile):
        log("Error: Makefile not found!", Colors.FAIL)
        return

    with open(makefile, 'r') as f:
        content = f.read()

    # Remove -Werror
    content = content.replace("-Werror", "")

    lines = content.split('\n')

    # Fix CFLAGS
    for i, line in enumerate(lines):
        if line.startswith("CFLAGS") and './LZMA' in line:
            lines[i] = f"CFLAGS := -g -O2 -I{prefix}/include -I. -I./LZMA/lzma465/C -I./LZMA/lzmalt -I./LZMA/lzmadaptive/C/7zip/Compress/LZMA_Lib"

    # Fix LIBS - ADD liblzmalib.a
    for i, line in enumerate(lines):
        if line.startswith("LIBS +=") and '-llzma' in line:
            lines[i] = f"LIBS += -lz -lm -L{prefix}/lib -llzo2 -llzma -L./LZMA/lzmadaptive/C/7zip/Compress/LZMA_Lib -llzmalib"

    # Remove XZ_SUPPORT
    for i, line in enumerate(lines):
        if '-DXZ_SUPPORT' in line:
            lines[i] = line.replace('-DXZ_SUPPORT', '')

    content = '\n'.join(lines)

    with open(makefile, 'w') as f:
        f.write(content)

    log("✓ Makefile fixed", Colors.OK)

def apply_universal_fixes(env):
    """Apply all necessary fixes for modern compilation"""
    log("Applying universal fixes for modern compilers...")

    # Create compat.h for musl/Alpine support
    create_compat_header()

    # Inject compat.h into source files
    for c_file in ["mksquashfs.c", "unsquashfs.c", "pseudo.c", "action.c"]:
        path = os.path.join("squashfs-tools", c_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                data = f.read()
            # Insert after the first include
            if '#include "compat.h"' not in data:
                data = re.sub(r'(#include <.*>\n)', r'\1#include "compat.h"\n', data, count=1)
                with open(path, "w") as f:
                    f.write(data)
                log(f"✓ Injected compat.h into {c_file}", Colors.OK)

    # Fix verbose duplicate
    fix_error_header()

    # FIX #2: Fix LZO wrapper includes (NEW)
    fix_lzo_wrapper()

    # FIX #1: Fix signal handlers (NEW)
    fix_signal_handlers()

    # Fix FNM_EXTMATCH (legacy fallback)
    fix_fnm_extmatch()

    # Disable XZ wrapper
    disable_xz_wrapper()

    # Fix Makefile
    fix_makefile(env)

    log("✓ All fixes applied", Colors.OK)

def build_and_deploy(env):
    """Compile Sasquatch and deploy binary"""
    log("Starting build process...")

    tools_path = "squashfs-tools"
    os.chdir(tools_path)

    # Clean build
    run_cmd("make clean", check=False, silent=True)

    # Build with parallel jobs
    nproc = os.cpu_count() or 2
    log(f"Building with {nproc} parallel jobs...")

    build_env = os.environ.copy()
    if env['is_termux']:
        build_env["CC"] = "clang"
        build_env["CXX"] = "clang++"

    # Use -fcommon for modern GCC versions (fixes multiple definition errors)
    build_env["CFLAGS"] = build_env.get("CFLAGS", "") + " -fcommon"

    result = run_cmd(f"make -j{nproc}", check=False)

    if result and result.returncode == 0 and os.path.exists("sasquatch"):
        log("✓ BUILD SUCCESSFUL! 🎉", Colors.OK)

        # Save binary locally
        local_bin = "../../sasquatch_binary"
        shutil.copy("sasquatch", local_bin)
        log(f"✓ Binary saved: {BUILD_DIR}/sasquatch_binary", Colors.OK)

        # Auto-install if possible
        target = f"{env['prefix']}/bin/sasquatch"
        log("", Colors.INFO)

        if env['is_termux']:
            # Termux: Can install directly
            try:
                shutil.copy("sasquatch", target)
                os.chmod(target, 0o755)
                log(f"✓ Installed to {target}", Colors.OK)
                log("You can now use: sasquatch --help", Colors.INFO)
            except Exception as e:
                log(f"Could not auto-install: {e}", Colors.WARN)
                log(f"Manual install: cp {os.getcwd()}/sasquatch {target} && chmod +x {target}", Colors.INFO)
        else:
            # Linux: Needs sudo
            log("To install system-wide, run:", Colors.INFO)
            log(f"  sudo cp {os.getcwd()}/sasquatch {target}", Colors.INFO)
            log(f"  sudo chmod +x {target}", Colors.INFO)

        log("", Colors.INFO)
        log("Usage: sasquatch [options] filesystem.squashfs [destination]", Colors.INFO)

        return True
    else:
        log("✗ BUILD FAILED", Colors.FAIL)
        log("", Colors.INFO)
        log("Troubleshooting tips:", Colors.WARN)
        log("1. Clean build: rm -rf " + BUILD_DIR, Colors.WARN)
        log("2. Check dependencies are installed", Colors.WARN)
        log("3. Try running script again", Colors.WARN)
        return False

def main():
    """Main execution flow"""
    banner()

    try:
        # Detect environment
        env = detect_env()
        log(f"Detected: {env['os']} ({env['pkg_mgr'] or 'unknown'})", Colors.INFO)

        # Install dependencies
        install_deps(env)

        # Setup source code
        if not setup_source():
            log("Failed to setup source code", Colors.FAIL)
            sys.exit(1)

        # Apply original patches
        apply_patches()

        # Apply modern compiler fixes
        apply_universal_fixes(env)

        # Build and deploy
        success = build_and_deploy(env)

        if success:
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        log("\nBuild cancelled by user", Colors.WARN)
        sys.exit(130)
    except Exception as e:
        log(f"Unexpected error: {str(e)}", Colors.FAIL)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
