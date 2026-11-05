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


# ---------------------------------------------------------------- README (embeds sources, sample Q&A, disclaimer)
def _block(path):
    return open(os.path.join(root, path), encoding="utf-8").read().strip()

src_rows = ["| ID | Title | Publisher | Status | URL |", "|---|---|---|---|---|"]
for i, t, p, u, ty, st_ in SOURCES:
    src_rows.append(f"| {i} | {t} | {p} | {st_} | {u} |")
sample = "\n".join(out[1:]).replace("## ", "### ")
disclaimer = _block("DISCLAIMER.md")

readme = f"""# Groww · Mutual Fund FAQ Assistant (facts-only RAG)

A small chat app that answers *factual* questions about four HDFC Mutual Fund schemes using only official public pages (HDFC Mutual Fund, SEBI, AMFI). Every answer is at most 3 sentences, carries exactly one source link and a "Last updated from sources" date. It refuses advice, does not quote returns/NAV, and rejects messages containing personal details.

- **Product context:** Groww (the assistant is the kind of FAQ widget a Groww-style app would embed).
- **AMC:** HDFC Mutual Fund. **Schemes:** HDFC Large Cap Fund, HDFC Flexi Cap Fund, HDFC ELSS Tax Saver, HDFC Mid Cap Fund.
- **Live app:** https://hdfc-mf-faq-assistant.streamlit.app/
- **Corpus:** {len(SOURCES)} public pages (listed below).

## Setup
```bash
python3 -m pip install -r requirements.txt
python3 -m unittest test_engine      # 20 tests
python3 -m streamlit run app.py
```
Optional wording layer: set `ANTHROPIC_API_KEY` (model via `MF_FAQ_MODEL`). Output is validated (max 3 sentences, no links, no new numbers) and falls back to the retrieved text. Without a key the app is fully rule-based and deterministic.

Hosting: push this folder to GitHub, then deploy on Streamlit Community Cloud with `app.py` as the main file.

## How it maps to the milestone themes
- **W1, Thinking like a model:** `engine.answer()` identifies the fact and scheme asked, then decides in order: personal details, advice refusal, returns/NAV redirect, out-of-scope fund, clarifying question, then answer. Covered by `test_engine.py`.
- **W2, LLMs and prompting:** fixed, polite refusal wording with an educational link; one consistent citation format; a concise grounded prompt in `llm.py` (optional, validated output).
- **W3, RAG only:** BM25 retrieval over a small curated corpus with scheme and topic boosting; every chunk carries exactly one URL from the source list, and a test checks that.

## Files
`app.py` UI, `engine.py` guardrails and retrieval, `corpus_data.py` sources and facts, `llm.py` optional wording, `test_engine.py`, `sources.csv` / `sources.md`, `sample_qa.md`, `DISCLAIMER.md`, `scripts/make_outputs.py` (regenerates the CSV, sample Q&A and this README).

## Disclaimer (as shown in the UI)
{disclaimer}

## Source list ({len(SOURCES)} pages, checked {RETRIEVED_ON})
Status: **opened** = page read in full on the check date; **linked** = linked from an opened official page, not yet opened.

""" + "\n".join(src_rows) + f"""

## Sample Q&A (generated from the real engine)
""" + sample + """
## Known limits
- The corpus is a **hand-curated snapshot dated """ + RETRIEVED_ON + """**; fees such as TER and exit load change, so re-check before relying on it. Nothing is scraped at runtime.
- TER shown is from the Direct Plan page; the Regular Plan differs.
- The capital-gains statement answer cites an HDFC Mutual Fund guide whose URL contains `/learn/blog/`. It is published by the AMC itself (first-party), not a third-party blog.
- Sources marked `linked` (other KIM/SID PDFs, SEBI investor page, AMFI introduction page) were not opened during the build; please click them.
- KIM/SID PDFs are cited for "where is the document" questions but their text is not searched.
- The benchmark riskometer level is not captured (image only).
- The optional LLM layer is untested.
- Not covered: other AMCs/schemes, performance, tax advice, account-specific queries.
"""
open(os.path.join(root, "README.md"), "w", encoding="utf-8").write(readme)
print("readme ok")
