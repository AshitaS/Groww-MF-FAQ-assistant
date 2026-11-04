"""Generate sources.csv, sources.md and sample_qa.md from the real corpus/engine."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from corpus_data import SOURCES, RETRIEVED_ON
from engine import answer

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(root, "sources.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "title", "publisher", "url", "type", "verification_status", "retrieved_on"])
    for s in SOURCES:
        w.writerow([*s, RETRIEVED_ON])

QS = [
    "What is the ELSS lock-in period?",
    "What is the exit load of HDFC Flexi Cap Fund?",
    "What is the minimum SIP for HDFC Mid Cap Fund?",
    "What is the expense ratio of HDFC Large Cap Fund?",
    "What is the benchmark of HDFC Flexi Cap Fund?",
    "What is the riskometer level of HDFC ELSS Tax Saver?",
    "How do I download my capital gains statement?",
    "Should I buy HDFC Flexi Cap Fund?",
    "What are the returns of HDFC Mid Cap Fund?",
    "My PAN is ABCDE1234F, send my statement",
]
out = [f"# Sample Q&A (generated from the real engine, data as of {RETRIEVED_ON})\n"]
for i, q in enumerate(QS, 1):
    r = answer(q, use_llm=False)
    shown = "(message withheld: contains personal details)" if r.kind == "pii" else q
    out.append(f"## {i}. {shown}\n*Type: {r.kind}*\n\n{r.text}\n\nSource: {r.link}\nLast updated from sources: {r.updated}\n")
open(os.path.join(root, "sample_qa.md"), "w", encoding="utf-8").write("\n".join(out))
print("ok")
