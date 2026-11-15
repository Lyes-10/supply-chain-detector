import Levenshtein

POPULAR_PACKAGES = [
    "requests", "numpy", "flask",          # kept for general coverage (Python ecosystem)
    "lodash", "express", "axios", "react",
    "dayjs", "jest", "mongoose", "prettier", "eslint",
    "commander", "uuid", "chalk", "vite", "nodemon",
    "redux", "typescript", "yargs", "socket.io",
    "dotenv", "moment",
]

def check_name_similarity(pkg_name, threshold=2):
    findings = []
    for popular in POPULAR_PACKAGES:
        if pkg_name.lower() == popular.lower():
            continue
        dist = Levenshtein.distance(pkg_name.lower(), popular.lower())
        if dist <= threshold:
            findings.append(f"Name '{pkg_name}' is {dist} edit(s) from popular package '{popular}'")
    return findings