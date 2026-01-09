#!/usr/bin/env python3
"""
SASQUATCH UNIVERSAL BUILDER - RC 1
------------------------------------------------------------
Developer: M-Tarantino
Original Logic: Craig Heffner (devttys0)
License: GNU General Public License v2 (GPLv2)

Description: 
This script automates the compilation of Sasquatch on modern 
Linux systems (Debian, Arch, etc.) and Termux. It dynamically 
patches legacy C code to comply with modern GCC/Clang standards.
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
    print("      SASQUATCH UNIVERSAL BUILDER - RC 1")
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
        info['packages'] = ['git', 'patch', 'make', 'clang', 'zlib', 'liblzma', 'xz-utils', 'lzo', 'lzo2', 'binutils', 'wget']
    # Check for Debian/Ubuntu
    elif shutil.which('apt'):
        info['pkg_mgr'] = 'apt'
        info['prefix'] = '/usr'
        info['packages'] = ['git', 'patch', 'make', 'gcc', 'g++', 'zlib1g-dev', 'liblzma-dev', 'liblzo2-dev', 'binutils', 'wget']
    # Check for Arch Linux
    elif shutil.which('pacman'):
        info['pkg_mgr'] = 'pacman'
        info['prefix'] = '/usr'
        info['packages'] = ['git', 'patch', 'make', 'gcc', 'zlib', 'xz', 'lzo', 'binutils', 'wget']
    # Check for Fedora/RHEL
    elif shutil.which('dnf'):
        info['pkg_mgr'] = 'dnf'
        info['prefix'] = '/usr'
        info['packages'] = ['git', 'patch', 'make', 'gcc', 'gcc-c++', 'zlib-devel', 'xz-devel', 'lzo-devel', 'binutils', 'wget']
    # Check for Alpine
    elif shutil.which('apk'):
        info['pkg_mgr'] = 'apk'
        info['prefix'] = '/usr'
        info['packages'] = ['git', 'patch', 'make', 'gcc', 'g++', 'zlib-dev', 'xz-dev', 'lzo-dev', 'binutils', 'wget']
    
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
    run_cmd(f"git clone {REPO_URL} repo", silent=True)
    
    log("Downloading SquashFS 4.3...")
    run_cmd(f"wget -q {SQUASHFS_URL}")
    
    log("Extracting archive...")
    run_cmd("tar -zxf squashfs4.3.tar.gz")
    
    log("✓ Source code ready", Colors.OK)

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

def fix_fnm_extmatch():
    """Fix FNM_EXTMATCH compatibility"""
    log("Fixing FNM_EXTMATCH compatibility...")
    
    tools_path = "squashfs-tools"
    unsquashfs_c = os.path.join(tools_path, "unsquashfs.c")
    
    if os.path.exists(unsquashfs_c):
        with open(unsquashfs_c, 'r') as f:
            content = f.read()
        
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
    
    fix_error_header()
    fix_fnm_extmatch()
    disable_xz_wrapper()
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
    
    result = run_cmd(f"make -j{nproc}")
    
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
        setup_source()
        
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