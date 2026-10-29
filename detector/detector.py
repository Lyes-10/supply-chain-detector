import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from checks.name_similarity import check_name_similarity
from checks.script_analysis import check_install_scripts

def scan_package(pkg_name, package_json_path):
    findings = []
    findings += check_name_similarity(pkg_name)
    findings += check_install_scripts(package_json_path)

    score = len(findings) * 2
    verdict = "SUSPICIOUS" if score >= 4 else "LOW RISK" if score > 0 else "CLEAN"

    print(f"\n--- Scan report: {pkg_name} ---")
    print(f"Risk score: {score}  ->  {verdict}")
    for f in findings:
        print(f" - {f}")
    return score, findings

if __name__ == "__main__":
    scan_package(
        pkg_name="reqeusts",
        package_json_path=os.path.expanduser("~/supply-chain-project/demo-malicious-pkg/package.json")
    )