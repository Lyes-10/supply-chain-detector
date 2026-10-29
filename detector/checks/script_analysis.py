import re
import json
import os

SUSPICIOUS_PATTERNS = [
    (r'require\([\'"]http[\'"]\)', "Network module imported"),
    (r'require\([\'"]child_process[\'"]\)', "Shell execution module imported"),
    (r'eval\(', "Use of eval()"),
    (r'Buffer\.from\(.+,\s*[\'"]base64[\'"]\)', "Base64-decoded buffer (possible obfuscation)"),
    (r'curl\s|wget\s', "Shell download command"),
]

def check_install_scripts(package_json_path):
    findings = []
    pkg_dir = os.path.dirname(package_json_path)

    with open(package_json_path) as f:
        pkg = json.load(f)
    scripts = pkg.get("scripts", {})

    hook_script = None
    if "postinstall" in scripts:
        findings.append(f"Package defines postinstall hook: {scripts['postinstall']}")
        hook_script = scripts["postinstall"]
    if "preinstall" in scripts:
        findings.append(f"Package defines preinstall hook: {scripts['preinstall']}")
        hook_script = scripts.get("preinstall", hook_script)

    if hook_script:
        parts = hook_script.split()
        for part in parts:
            if part.endswith(".js"):
                script_path = os.path.join(pkg_dir, part.lstrip("./"))
                if os.path.exists(script_path):
                    with open(script_path) as f:
                        content = f.read()
                    for pattern, label in SUSPICIOUS_PATTERNS:
                        if re.search(pattern, content):
                            findings.append(f"{label} found in {part}")
    return findings