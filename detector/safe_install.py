import subprocess
import sys
import os
import glob
import tarfile
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detector import scan_package

def safe_install(pkg_name, registry):
    tmpdir = tempfile.mkdtemp(prefix="safe_install_")
    try:
        print(f"[*] Downloading '{pkg_name}' from {registry} for inspection (not installing yet)...")
        result = subprocess.run(
            ["npm", "pack", pkg_name, "--registry", registry],
            cwd=tmpdir, capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"[!] Could not download package '{pkg_name}':\n{result.stderr}")
            sys.exit(1)

        tarballs = glob.glob(os.path.join(tmpdir, "*.tgz"))
        if not tarballs:
            print("[!] No tarball downloaded, cannot scan.")
            sys.exit(1)

        extract_dir = os.path.join(tmpdir, "extracted")
        with tarfile.open(tarballs[0]) as tar:
            tar.extractall(extract_dir)

        pkg_json = os.path.join(extract_dir, "package", "package.json")
        if not os.path.exists(pkg_json):
            print("[!] package.json not found inside tarball, cannot scan.")
            sys.exit(1)

        score, findings = scan_package(pkg_name, pkg_json)

        if score >= 4:
            print(f"\n BLOCKED: '{pkg_name}' scored {score} -> SUSPICIOUS.")
            print("Installation aborted. This package was NOT installed on your system.")
            sys.exit(1)
        else:
            verdict = "LOW RISK" if score > 0 else "CLEAN"
            print(f"\n '{pkg_name}' passed the scan (score={score} -> {verdict}).")
            print("[*] Proceeding with real installation...\n")
            subprocess.run(["npm", "install", pkg_name, "--registry", registry], check=True)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 safe_install.py <package-name> <registry-url>")
        sys.exit(1)
    safe_install(sys.argv[1], sys.argv[2])
