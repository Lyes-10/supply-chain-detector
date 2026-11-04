import sys, os, glob, json
sys.path.insert(0, os.path.dirname(__file__))
from detector import scan_package

THRESHOLD = 4  # matches detector.py's SUSPICIOUS cutoff

def scan_dir(path):
    results = []
    for pj in glob.glob(os.path.join(path, "*", "package.json")):
        name = os.path.basename(os.path.dirname(pj))
        score, findings = scan_package(name, pj)
        results.append((name, score, findings))
    return results

mal_dir = os.path.expanduser("~/supply-chain-project/malicious-packages")
benign_dir = os.path.expanduser("~/supply-chain-project/test-packages")

print("\n################ MALICIOUS SET ################")
mal_results = scan_dir(mal_dir)
tp = sum(1 for _, s, _ in mal_results if s >= THRESHOLD)
fn = len(mal_results) - tp

print("\n################ BENIGN SET ################")
benign_results = scan_dir(benign_dir)
fp = sum(1 for _, s, _ in benign_results if s >= THRESHOLD)
tn = len(benign_results) - fp

precision = tp / (tp + fp) if (tp + fp) else 0
recall = tp / (tp + fn) if (tp + fn) else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

print("\n################ METRICS ################")
print(f"Malicious samples: {len(mal_results)}  (TP={tp}, FN={fn})")
print(f"Benign samples:    {len(benign_results)}  (TN={tn}, FP={fp})")
print(f"Precision: {precision:.2f}")
print(f"Recall:    {recall:.2f}")
print(f"F1 score:  {f1:.2f}")
